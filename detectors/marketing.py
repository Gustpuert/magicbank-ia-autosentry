import requests
from bs4 import BeautifulSoup
from datetime import datetime

from detectors.base import BaseDetector
from core.event import DetectionEvent


class MarketingDetector(BaseDetector):

    def detect(self):
        events = []

        events += self.detect_google_blog()
        events += self.detect_meta_news()

        return events


    def fetch(self, url):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print("[FETCH ERROR]", e)
        return None


    def detect_google_blog(self):
        url = "https://blog.google"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        for article in soup.select("a")[:15]:
            title = article.get_text(strip=True)

            if self.is_relevant(title):
                events.append(self.build_event(title, url))

        return events


    def detect_meta_news(self):
        url = "https://www.meta.com/news"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        for article in soup.select("a")[:15]:
            title = article.get_text(strip=True)

            if self.is_relevant(title):
                events.append(self.build_event(title, url))

        return events


    def is_relevant(self, title):
        if not title:
            return False

        title = title.lower()

        keywords = [
            "update",
            "launch",
            "new",
            "feature",
            "ai",
            "ads",
            "marketing"
        ]

        return any(k in title for k in keywords)


    def build_event(self, title, source):
        return DetectionEvent(
            faculty="marketing",
            jurisdiction="GLOBAL",
            source_url=source,
            title=title,
            document_type="Actualización",
            publication_date=datetime.utcnow().date().isoformat()
        )
