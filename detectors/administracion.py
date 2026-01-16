from detectors.base import BaseDetector
from core.event import DetectionEvent


class AdministracionDetector(BaseDetector):
    def detect(self):
        events = []

        sources = [
            "https://www.funcionpublica.gov.co",
            "https://www.mincit.gov.co"
        ]

        for source in sources:
            event = DetectionEvent(
                faculty="administracion",
                jurisdiction="CO",
                source_url=source,
                title="Actualización normativa en gestión empresarial",
                document_type="Resolución",
                publication_date="2026-01-01"
            )
            events.append(event)

        return events
