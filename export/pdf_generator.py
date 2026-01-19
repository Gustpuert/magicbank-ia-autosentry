from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT
from datetime import datetime
import json
from pathlib import Path


class PDFHistoryGenerator:
    """
    Generador oficial de PDF para el historial de Magic Bank.
    """

    def __init__(self, history_path: str = "registry/history.json"):
        self.history_path = Path(history_path)

        if not self.history_path.exists():
            raise FileNotFoundError("No existe el historial para generar el PDF.")

    # ==========================
    # CARGA DE HISTORIAL
    # ==========================
    def _load_history(self):
        with open(self.history_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ==========================
    # GENERACIÓN DE PDF
    # ==========================
    def generate_pdf(self, output_path: str):
        data = self._load_history()
        events = data.get("events", [])

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        normal = styles["Normal"]
        title = styles["Title"]

        content = []

        # Título
        content.append(Paragraph("MAGIC BANK", title))
        content.append(Spacer(1, 12))

        content.append(Paragraph(
            "Historial Oficial de Actualizaciones Académicas",
            styles["Heading2"]
        ))
        content.append(Spacer(1, 12))

        content.append(Paragraph(
            f"Fecha de generación: {datetime.utcnow().isoformat()} UTC",
            normal
        ))
        content.append(Spacer(1, 20))

        # Contenido
        if not events:
            content.append(Paragraph(
                "No existen registros de actualización.",
                normal
            ))
        else:
            for idx, entry in enumerate(events, start=1):
                event = entry.get("event", {})

                block = f"""
                <b>{idx}. {event.get('entidad', 'Entidad no definida')}</b><br/>
                <b>Área:</b> {event.get('rama', 'N/D')}<br/>
                <b>País:</b> {event.get('pais', 'N/D')}<br/>
                <b>Fuente:</b> {event.get('fuente', 'N/D')}<br/>
                <b>Estado:</b> {event.get('estado', 'N/D')}<br/>
                <b>Fecha de registro:</b> {entry.get('timestamp', 'N/D')}
                """

                content.append(Paragraph(block, normal))
                content.append(Spacer(1, 14))

        # Pie
        content.append(Spacer(1, 30))
        content.append(Paragraph(
            "Documento generado automáticamente por Magic Bank.",
            styles["Italic"]
        ))

        doc.build(content)

        return output_path
