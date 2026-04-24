from datetime import datetime
import uuid


class DetectionEvent:
    def __init__(
        self,
        faculty,
        jurisdiction,
        source_url,
        title,
        document_type,
        publication_date,
        effective_date=None
    ):
        self.id = str(uuid.uuid4())  # 🔥 ID único

        self.faculty = faculty
        self.jurisdiction = jurisdiction
        self.source_url = source_url
        self.title = title
        self.document_type = document_type
        self.publication_date = publication_date
        self.effective_date = effective_date

        self.detected_at = datetime.utcnow().isoformat()  # 🔥 ya normalizado
        self.relevance = None

    def to_dict(self):
        return {
            "id": self.id,
            "faculty": self.faculty,
            "jurisdiction": self.jurisdiction,
            "source_url": self.source_url,
            "title": self.title,
            "document_type": self.document_type,
            "publication_date": self.publication_date,
            "effective_date": self.effective_date,
            "detected_at": self.detected_at,
            "relevance": self.relevance
        }
