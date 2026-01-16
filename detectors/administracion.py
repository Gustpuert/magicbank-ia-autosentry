from detectors.base import BaseDetector
from core.event import DetectionEvent
from datetime import datetime

class AdministracionDetector(BaseDetector):
    def detect(self):
        events = []

        for source in self.sources:
            event = DetectionEvent(
                faculty="administracion",
                jurisdiction="CO",
                source_url=source,
                title="Actualización normativa en gestión empresarial",
                document_type="Resolución",
                publication_date="2026-01-01",
                detected_at=datetime.utcnow().isoformat(),
                relevance="medium"
            )
            events.append(event)

        return events
