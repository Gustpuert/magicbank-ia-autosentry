from detectors.base import BaseDetector
from core.event import DetectionEvent


class TributarioDetector(BaseDetector):
    def detect(self):
        events = []

        sources = [
            "https://www.dian.gov.co"
        ]

        for source in sources:
            event = DetectionEvent(
                faculty="tributario",
                jurisdiction="CO",
                source_url=source,
                title="Actualización tributaria relevante",
                document_type="Resolución",
                publication_date="2026-01-01"
            )
            events.append(event)

        return events
