import requests
import hashlib
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

from detectors.base import BaseDetector
from core.event import DetectionEvent


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s"
)


class TributarioDetector(BaseDetector):
    """
    MAGICBANK SUPREME — Tributary Normative Intelligence Detector

    Jurisdictions:
    - CO (DIAN, MinHacienda, UGPP)
    - US (IRS)
    - CA (CRA)

    Core Objectives:
    - Official source prioritization
    - Real normative relevance
    - Event deduplication
    - Severity classification
    - Real publication date extraction
    - Institutional logging
    """

    TRIBUTARY_SOURCES = {
        "CO": [
            {
                "name": "DIAN Normatividad",
                "url": "https://www.dian.gov.co/normatividad/Paginas/default.aspx",
                "source_type": "official"
            },
            {
                "name": "DIAN Facturación Electrónica",
                "url": "https://www.dian.gov.co/impuestos/factura-electronica",
                "source_type": "official"
            }
        ],
        "US": [
            {
                "name": "IRS News",
                "url": "https://www.irs.gov/newsroom",
                "source_type": "official"
            }
        ],
        "CA": [
            {
                "name": "CRA News",
                "url": "https://www.canada.ca/en/revenue-agency/news.html",
                "source_type": "official"
            }
        ]
    }

    KEYWORDS = {
        "critical": [
            "reforma",
            "resolución",
            "decreto",
            "ley",
            "mandatory",
            "obligatorio",
            "irs update",
            "compliance"
        ],
        "important": [
            "impuesto",
            "tributario",
            "declaración",
            "retención",
            "facturación",
            "tax",
            "filing",
            "withholding"
        ],
        "informational": [
            "calendario",
            "recordatorio",
            "guidance",
            "notice"
        ]
    }

    def __init__(self):
        super().__init__()
        self.seen_hashes = set()

    # =========================
    # MAIN DETECTION
    # =========================
    def detect(self):
        events = []

        for jurisdiction, sources in self.TRIBUTARY_SOURCES.items():
            for source in sources:
                events += self.detect_source(
                    jurisdiction=jurisdiction,
                    source_name=source["name"],
                    source_url=source["url"]
                )

        return events

    # =========================
    # FETCH LAYER
    # =========================
    def fetch(self, url):
        headers = {
            "User-Agent": "MagicBankNormativeBot/1.0"
        }

        try:
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                logging.info(f"Fetched successfully: {url}")
                return response.text

            logging.warning(f"Non-200 status ({response.status_code}) for {url}")

        except requests.exceptions.Timeout:
            logging.error(f"Timeout while fetching {url}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for {url}: {e}")

        return None

    # =========================
    # SOURCE DETECTION
    # =========================
    def detect_source(self, jurisdiction, source_name, source_url):
        html = self.fetch(source_url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        for link in soup.find_all("a", href=True)[:100]:
            title = link.get_text(strip=True)
            href = urljoin(source_url, link["href"])

            if not title:
                continue

            relevance = self.evaluate_relevance(title, href)

            if not relevance:
                continue

            event_hash = self.generate_hash(title, href)

            if event_hash in self.seen_hashes:
                continue

            self.seen_hashes.add(event_hash)

            publication_date = self.extract_publication_date(link)

            events.append(
                self.build_event(
                    title=title,
                    source=href,
                    jurisdiction=jurisdiction,
                    severity=relevance,
                    publication_date=publication_date,
                    source_name=source_name
                )
            )

        return events

    # =========================
    # RELEVANCE ENGINE
    # =========================
    def evaluate_relevance(self, title, href):
        combined = f"{title} {href}".lower()

        for severity, keywords in self.KEYWORDS.items():
            if any(keyword in combined for keyword in keywords):
                return severity

        return None

    # =========================
    # DATE EXTRACTION
    # =========================
    def extract_publication_date(self, link):
        """
        Attempts:
        1. datetime attr
        2. nearby text
        3. fallback to detection date
        """

        if link.has_attr("datetime"):
            return link["datetime"]

        parent_text = link.parent.get_text(" ", strip=True)

        for token in parent_text.split():
            try:
                parsed = datetime.fromisoformat(token)
                return parsed.date().isoformat()
            except Exception:
                continue

        return datetime.utcnow().date().isoformat()

    # =========================
    # HASH / DEDUP
    # =========================
    def generate_hash(self, title, source):
        raw = f"{title}|{source}"
        return hashlib.sha256(raw.encode()).hexdigest()

    # =========================
    # EVENT BUILDER
    # =========================
    def build_event(
        self,
        title,
        source,
        jurisdiction,
        severity,
        publication_date,
        source_name
    ):
        document_type_map = {
            "critical": "Critical Tributary Update",
            "important": "Important Tributary Update",
            "informational": "Informational Tributary Update"
        }

        return DetectionEvent(
            faculty="tributario",
            jurisdiction=jurisdiction,
            source_url=source,
            source_name=source_name,
            title=title,
            document_type=document_type_map.get(
                severity,
                "Tributary Update"
            ),
            severity=severity,
            publication_date=publication_date,
            detection_date=datetime.utcnow().isoformat()
        )

    # =========================
    # OPTIONAL: IMPACT SCORE
    # =========================
    def score_event(self, event):
        severity_scores = {
            "critical": 100,
            "important": 70,
            "informational": 40
        }

        return severity_scores.get(
            getattr(event, "severity", "informational"),
            40
        )
