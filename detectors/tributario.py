from detectors.base import BaseDetector
from core.event import DetectionEvent

class TributarioDetector(BaseDetector):
    def detect(self):
        events = []

        for source in self.sources:
            event = DetectionEvent(
                faculty="contaduria",
                jurisdiction="CO",
                source_url=source,
                title="Actualización tributaria relevante",
                document_type="Resolución",
                publication_date="2026-01-01"
            )
            events.append(event)

        return events
