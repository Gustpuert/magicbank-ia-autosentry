from datetime import datetime
from pathlib import Path
from export.pdf_generator import PDFHistoryGenerator
from export.pdf_signer import PDFSigner


class AutoHistoryExporter:
    def __init__(self):
        self.output_dir = Path("exports")
        self.output_dir.mkdir(exist_ok=True)

    def run(self):
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        pdf_path = self.output_dir / f"historial_magicbank_{timestamp}.pdf"

        generator = PDFHistoryGenerator()
        generator.generate_pdf(str(pdf_path))

        signer = PDFSigner()
        signature = signer.sign_file(str(pdf_path))

        return {
            "pdf": pdf_path,
            "signature": signature
        }
