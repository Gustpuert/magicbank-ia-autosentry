import requests
from bs4 import BeautifulSoup
from datetime import datetime

from detectors.base import BaseDetector
from core.event import DetectionEvent


class DerechoUSADetector(BaseDetector):

    def detect(self):
        events = []

        print("[INFO] Derecho USA Detector iniciado")

        events += self.congress()
        events += self.supreme_court()
        events += self.irs()

        print(f"[INFO] USA encontró {len(events)} eventos")

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
    # 🏛️ CONGRESS (LEYES)
    # =========================
    def congress(self):
        url = "https://www.congress.gov"
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
    # ⚖️ SUPREME COURT
    # =========================
    def supreme_court(self):
        url = "https://www.supremecourt.gov/opinions/opinions.aspx"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        rows = soup.select("table tr")

        for row in rows[:20]:
            cols = row.find_all("td")

            if len(cols) < 1:
                continue

            title = row.get_text(strip=True)

            if self.is_legal_relevant(title):
                events.append(self.build_event(title, url, "derecho"))

        return events


    # =========================
    # 💰 IRS (TRIBUTARIO)
    # =========================
    def irs(self):
        url = "https://www.irs.gov/newsroom"
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
            "law", "act", "bill", "tax",
            "regulation", "court", "justice",
            "decision", "ruling"
        ]

        return any(k in title for k in keywords)


    def build_event(self, title, source, faculty):
        return DetectionEvent(
            faculty=faculty,
            jurisdiction="US",
            source_url=source,
            title=title,
            document_type="Legal update",
            publication_date=datetime.utcnow().date().isoformat()
        )
