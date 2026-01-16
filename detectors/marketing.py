from detectors.base import BaseDetector
from core.event import DetectionEvent


class MarketingDetector(BaseDetector):
    def detect(self):
        events = []

        sources = [
            "https://blog.google",
            "https://www.meta.com/news"
        ]

        for source in sources:
            event = DetectionEvent(
                faculty="marketing",
                jurisdiction="GLOBAL",
                source_url=source,
                title="Nueva funcionalidad en plataforma digital",
                document_type="Actualización",
                publication_date="2026-01-01"
            )
            events.append(event)

        return events
