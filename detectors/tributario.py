import requests
from bs4 import BeautifulSoup
from datetime import datetime

from detectors.base import BaseDetector
from core.event import DetectionEvent


class TributarioDetector(BaseDetector):

    def detect(self):
        events = []
        events += self.detect_dian()
        return events


    def fetch(self, url):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print("[FETCH ERROR]", e)
        return None


    def detect_dian(self):
        url = "https://www.dian.gov.co"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        for link in soup.select("a")[:20]:
            title = link.get_text(strip=True)

            if self.is_relevant(title):
                events.append(self.build_event(title, url))

        return events


    def is_relevant(self, title):
        if not title:
            return False

        title = title.lower()

        keywords = [
            "resolución",
            "impuesto",
            "tributario",
            "dian",
            "declaración",
            "retención",
            "facturación"
        ]

        return any(k in title for k in keywords)


    def build_event(self, title, source):
        return DetectionEvent(
            faculty="tributario",
            jurisdiction="CO",
            source_url=source,
            title=title,
            document_type="Actualización tributaria",
            publication_date=datetime.utcnow().date().isoformat()
        )
