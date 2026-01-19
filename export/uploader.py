from pathlib import Path
from datetime import datetime
import shutil


class HistoryUploader:
    """
    Publica automáticamente los PDFs firmados
    en el repositorio oficial de Magic Bank.
    """

    def __init__(self):
        self.publish_dir = Path("published/history")
        self.publish_dir.mkdir(parents=True, exist_ok=True)

    def upload(self, pdf_path: str, signature_path: str):
        pdf_path = Path(pdf_path)
        signature_path = Path(signature_path)

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        pdf_target = self.publish_dir / f"{timestamp}_{pdf_path.name}"
        sig_target = self.publish_dir / f"{timestamp}_{signature_path.name}"

        shutil.copy2(pdf_path, pdf_target)
        shutil.copy2(signature_path, sig_target)

        return {
            "pdf": str(pdf_target),
            "signature": str(sig_target),
            "status": "published"
        }
