import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime

from detectors.base import BaseDetector
from core.event import DetectionEvent


class DerechoDetector(BaseDetector):

    def detect(self):
        events = []
        events += self.funcion_publica()
        events += self.senado()
        events += self.rss()
        return events

    def fetch(self, url):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print("[FETCH ERROR]", e)
        return None

    def funcion_publica(self):
        url = "https://www.funcionpublica.gov.co"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        for a in soup.select("a")[:30]:
            title = a.get_text(strip=True)

            if self.is_legal(title):
                events.append(self.build(title, url, "Norma"))

        return events

    def senado(self):
        url = "https://www.senado.gov.co"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        for a in soup.select("a")[:30]:
            title = a.get_text(strip=True)

            if self.is_legal(title):
                events.append(self.build(title, url, "Proyecto"))

        return events

    def rss(self):
        url = "https://www.funcionpublica.gov.co/rss"
        events = []

        try:
            feed = feedparser.parse(url)

            for e in feed.entries[:20]:
                title = e.title

                if self.is_legal(title):
                    events.append(self.build(title, url, "Publicación"))

        except Exception as e:
            print("[RSS ERROR]", e)

        return events

    def is_legal(self, title):
        if not title:
            return False

        title = title.lower()

        keywords = [
            "ley", "decreto", "sentencia",
            "reforma", "norma", "resolución"
        ]

        return any(k in title for k in keywords)

    def build(self, title, source, doc_type):
        return DetectionEvent(
            faculty="derecho",
            jurisdiction="CO",
            source_url=source,
            title=title,
            document_type=doc_type,
            publication_date=datetime.utcnow().date().isoformat()
        )
