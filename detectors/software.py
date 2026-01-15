from detectors.base import BaseDetector
from core.event import DetectionEvent

class SoftwareDetector(BaseDetector):
    def detect(self):
        events = []

        for source in self.sources:
            event = DetectionEvent(
                faculty="software",
                jurisdiction="GLOBAL",
                source_url=source,
                title="Nueva tecnología o framework relevante",
                document_type="Tecnología",
                publication_date="2026-01-01"
            )
            events.append(event)

        return events
