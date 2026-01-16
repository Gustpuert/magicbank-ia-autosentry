from detectors.base import BaseDetector
from core.event import DetectionEvent


class DerechoDetector(BaseDetector):
    def detect(self):
        events = []

        sources = [
            "https://www.funcionpublica.gov.co",
            "https://www.senado.gov.co"
        ]

        for source in sources:
            event = DetectionEvent(
                faculty="derecho",
                jurisdiction="CO",
                source_url=source,
                title="Nueva reforma legal publicada",
                document_type="Ley",
                publication_date="2026-01-01"
            )
            events.append(event)

        return events
