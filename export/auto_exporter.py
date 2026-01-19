from datetime import datetime
from pathlib import Path
from export.pdf_generator import PDFHistoryGenerator


class AutoHistoryExporter:
    """
    Automatiza la generación periódica del historial oficial.
    """

    def __init__(self):
        self.output_dir = Path("exports")
        self.output_dir.mkdir(exist_ok=True)

    def run(self):
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"historial_magicbank_{timestamp}.pdf"

        generator = PDFHistoryGenerator()
        generator.generate_pdf(str(output_file))

        return output_file
