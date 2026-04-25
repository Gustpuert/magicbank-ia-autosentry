import requests
from bs4 import BeautifulSoup
from datetime import datetime

from detectors.base import BaseDetector
from core.event import DetectionEvent


class DerechoCanadaDetector(BaseDetector):

    def detect(self):
        events = []

        print("[INFO] Derecho Canadá Detector iniciado")

        events += self.justice_laws()
        events += self.supreme_court()
        events += self.cra()

        print(f"[INFO] Canadá encontró {len(events)} eventos")

        return events


    def fetch(self, url):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print(f"[FETCH ERROR] {url}: {e}")
        return None


    # =========================
    # 📜 JUSTICE LAWS
    # =========================
    def justice_laws(self):
        url = "https://laws-lois.justice.gc.ca"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.select("a")[:40]:
            title = tag.get_text(strip=True)

            if self.is_legal_relevant(title):
                events.append(self.build_event(title, url, "derecho"))

        return events


    # =========================
    # ⚖️ SUPREME COURT CANADA
    # =========================
    def supreme_court(self):
        url = "https://www.scc-csc.ca"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.select("a")[:40]:
            title = tag.get_text(strip=True)

            if self.is_legal_relevant(title):
                events.append(self.build_event(title, url, "derecho"))

        return events


    # =========================
    # 💰 CRA (TRIBUTARIO)
    # =========================
    def cra(self):
        url = "https://www.canada.ca/en/revenue-agency.html"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.select("a")[:40]:
            title = tag.get_text(strip=True)

            if self.is_legal_relevant(title):
                events.append(self.build_event(title, url, "tributario"))

        return events


    def is_legal_relevant(self, title):
        if not title:
            return False

        title = title.lower()

        keywords = [
            "law", "act", "regulation",
            "tax", "court", "decision",
            "justice"
        ]

        return any(k in title for k in keywords)


    def build_event(self, title, source, faculty):
        return DetectionEvent(
            faculty=faculty,
            jurisdiction="CA",
            source_url=source,
            title=title,
            document_type="Legal update",
            publication_date=datetime.utcnow().date().isoformat()
        )
