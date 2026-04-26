import requests
import hashlib
import logging
import time
import json
import re

from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
from dateutil import parser as date_parser

from detectors.base import BaseDetector
from core.event import DetectionEvent


# =========================================================
# LOGGING CONFIGURATION
# =========================================================
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s"
)


class TributarioDetector(BaseDetector):
    """
    MAGICBANK SUPREME — Normative Intelligence Engine

    FEATURES:
    - Multi-jurisdiction (CO / US / CA)
    - Official source governance
    - Retry + backoff
    - Smart parsing
    - Weighted keyword scoring
    - Source-specific selectors
    - Historical persistence
    - Change detection
    - Deduplication
    - Severity governance
    - Institutional-grade event architecture
    """

    # =========================================================
    # CONFIG
    # =========================================================
    HISTORY_FILE = "tributario_detector_history.json"

    TRIBUTARY_SOURCES = {
        "CO": [
            {
                "name": "DIAN Normatividad",
                "url": "https://www.dian.gov.co/normatividad/Paginas/default.aspx",
                "selectors": [
                    "a",
                    ".list-group-item",
                    ".news-item a"
                ]
            },
            {
                "name": "DIAN Facturación Electrónica",
                "url": "https://www.dian.gov.co/impuestos/factura-electronica",
                "selectors": [
                    "a",
                    ".news-item a"
                ]
            }
        ],
        "US": [
            {
                "name": "IRS Newsroom",
                "url": "https://www.irs.gov/newsroom",
                "selectors": [
                    "a",
                    ".views-row a"
                ]
            }
        ],
        "CA": [
            {
                "name": "CRA News",
                "url": "https://www.canada.ca/en/revenue-agency/news.html",
                "selectors": [
                    "a",
                    ".gcwnws a"
                ]
            }
        ]
    }

    KEYWORDS = {
        "critical": {
            "reforma": 10,
            "resolución": 10,
            "decreto": 10,
            "ley": 10,
            "mandatory": 9,
            "obligatorio": 9,
            "compliance": 8,
            "sanction": 8,
            "penalty": 8
        },
        "important": {
            "impuesto": 7,
            "tributario": 7,
            "declaración": 7,
            "retención": 7,
            "facturación": 7,
            "tax": 7,
            "filing": 7,
            "withholding": 7,
            "irs": 6,
            "vat": 6
        },
        "informational": {
            "calendario": 4,
            "recordatorio": 4,
            "guidance": 4,
            "notice": 4,
            "boletín": 4
        }
    }

    # =========================================================
    # INIT
    # =========================================================
    def __init__(self):
        super().__init__()

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "MagicBankNormativeBot/2.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml"
        })

        self.seen_hashes = set()
        self.history = self.load_history()

    # =========================================================
    # MAIN
    # =========================================================
    def detect(self):
        events = []

        for jurisdiction, sources in self.TRIBUTARY_SOURCES.items():
            for source in sources:
                events.extend(
                    self.detect_source(
                        jurisdiction=jurisdiction,
                        source=source
                    )
                )

        self.save_history()

        return events

    # =========================================================
    # FETCH WITH RETRY + BACKOFF
    # =========================================================
    def fetch(self, url, retries=3, backoff=2):
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=20)

                if response.status_code == 200:
                    logging.info(f"Fetched successfully: {url}")
                    return response.text

                logging.warning(
                    f"Status {response.status_code} for {url}"
                )

            except requests.exceptions.Timeout:
                logging.error(f"Timeout on {url}")

            except requests.exceptions.RequestException as e:
                logging.error(f"Request error on {url}: {e}")

            sleep_time = backoff ** attempt
            logging.info(f"Retrying in {sleep_time}s...")
            time.sleep(sleep_time)

        return None

    # =========================================================
    # DETECT SOURCE
    # =========================================================
    def detect_source(self, jurisdiction, source):
        html = self.fetch(source["url"])

        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        events = []

        links = self.extract_links(soup, source)

        for link in links:
            title = link.get_text(" ", strip=True)

            if not title:
                continue

            href = urljoin(source["url"], link.get("href", ""))

            score, severity = self.evaluate_relevance(title, href)

            if score == 0:
                continue

            event_hash = self.generate_hash(title, href)

            if self.is_duplicate(event_hash):
                continue

            publication_date = self.extract_publication_date(link)

            change_type = self.detect_change_type(
                event_hash,
                title,
                publication_date
            )

            event = self.build_event(
                title=title,
                source=href,
                jurisdiction=jurisdiction,
                severity=severity,
                score=score,
                publication_date=publication_date,
                source_name=source["name"],
                change_type=change_type
            )

            events.append(event)

            self.register_event(
                event_hash,
                title,
                publication_date
            )

        return events

    # =========================================================
    # SMART LINK EXTRACTION
    # =========================================================
    def extract_links(self, soup, source):
        collected = []

        for selector in source.get("selectors", ["a"]):
            try:
                collected.extend(
                    soup.select(selector)
                )
            except Exception:
                continue

        unique_links = []

        seen = set()

        for link in collected:
            href = link.get("href")

            if not href:
                continue

            if href in seen:
                continue

            seen.add(href)
            unique_links.append(link)

        return unique_links[:150]

    # =========================================================
    # RELEVANCE ENGINE
    # =========================================================
    def evaluate_relevance(self, title, href):
        combined = f"{title} {href}".lower()

        best_score = 0
        best_severity = None

        for severity, words in self.KEYWORDS.items():
            score = 0

            for keyword, weight in words.items():
                if re.search(rf"\b{re.escape(keyword)}\b", combined):
                    score += weight

            if score > best_score:
                best_score = score
                best_severity = severity

        return best_score, best_severity

    # =========================================================
    # DATE PARSER
    # =========================================================
    def extract_publication_date(self, link):
        candidates = []

        if link.has_attr("datetime"):
            candidates.append(link["datetime"])

        parent_text = link.parent.get_text(" ", strip=True)
        candidates.append(parent_text)

        for candidate in candidates:
            try:
                parsed = date_parser.parse(
                    candidate,
                    fuzzy=True
                )

                return parsed.date().isoformat()

            except Exception:
                continue

        return datetime.utcnow().date().isoformat()

    # =========================================================
    # HASH
    # =========================================================
    def generate_hash(self, title, source):
        raw = f"{title}|{source}"
        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()

    # =========================================================
    # DUPLICATION
    # =========================================================
    def is_duplicate(self, event_hash):
        return event_hash in self.seen_hashes

    # =========================================================
    # CHANGE DETECTION
    # =========================================================
    def detect_change_type(
        self,
        event_hash,
        title,
        publication_date
    ):
        previous = self.history.get(event_hash)

        if not previous:
            return "new"

        if (
            previous.get("title") != title
            or previous.get("publication_date") != publication_date
        ):
            return "updated"

        return "existing"

    # =========================================================
    # HISTORY REGISTRATION
    # =========================================================
    def register_event(
        self,
        event_hash,
        title,
        publication_date
    ):
        self.seen_hashes.add(event_hash)

        self.history[event_hash] = {
            "title": title,
            "publication_date": publication_date,
            "last_seen": datetime.utcnow().isoformat()
        }

    # =========================================================
    # HISTORY LOAD
    # =========================================================
    def load_history(self):
        try:
            with open(self.HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception:
            return {}

    # =========================================================
    # HISTORY SAVE
    # =========================================================
    def save_history(self):
        try:
            with open(
                self.HISTORY_FILE,
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    self.history,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

        except Exception as e:
            logging.error(
                f"Failed to save history: {e}"
            )

    # =========================================================
    # EVENT BUILDER
    # =========================================================
    def build_event(
        self,
        title,
        source,
        jurisdiction,
        severity,
        score,
        publication_date,
        source_name,
        change_type
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
            impact_score=score,
            publication_date=publication_date,
            detection_date=datetime.utcnow().isoformat(),
            change_type=change_type
        )

    # =========================================================
    # GOVERNANCE SCORING
    # =========================================================
    def score_event(self, event):
        base_scores = {
            "critical": 100,
            "important": 70,
            "informational": 40
        }

        score = base_scores.get(
            getattr(event, "severity", "informational"),
            40
        )

        score += min(
            getattr(event, "impact_score", 0),
            25
        )

        if getattr(event, "change_type", "") == "new":
            score += 10

        elif getattr(event, "change_type", "") == "updated":
            score += 5

        return min(score, 100)
