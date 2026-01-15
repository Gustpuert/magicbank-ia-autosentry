from detectors.base import BaseDetector
from core.event import DetectionEvent

class MarketingDetector(BaseDetector):
    def detect(self):
        events = []

        for source in self.sources:
            event = DetectionEvent(
                faculty="marketing",
                jurisdiction="GLOBAL",
                source_url=source,
                title="Nueva funcionalidad en plataforma digital",
                document_type="Actualización de plataforma",
                publication_date="2026-01-01"
            )
            events.append(event)

        return events