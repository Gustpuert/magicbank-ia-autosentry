import json
from pathlib import Path
from datetime import datetime


class HistoryExporter:
    """
    Exportador oficial del historial de Magic Bank.
    Permite exportar en formato JSON o PDF (estructura preparada).
    """

    def __init__(self, history_path: str = "registry/history.json"):
        self.history_path = Path(history_path)

        if not self.history_path.exists():
            raise FileNotFoundError("No existe el historial para exportar.")

    # ================================
    # CARGA DE DATOS
    # ================================
    def _load_history(self):
        with open(self.history_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ================================
    # EXPORTACIÓN JSON (TÉCNICA)
    # ================================
    def export_json(self, output_path: str):
        data = self._load_history()

        export = {
            "generated_at": datetime.utcnow().isoformat(),
            "source": "Magic Bank",
            "type": "technical_history",
            "events": data.get("events", [])
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export, f, indent=2, ensure_ascii=False)

        return output_path

    # ================================
    # EXPORTACIÓN RESUMIDA (ALUMNO)
    # ================================
    def export_summary(self, output_path: str):
        data = self._load_history()
        events = data.get("events", [])

        summary = []
        for entry in events:
            event = entry.get("event", {})
            summary.append({
                "fecha": entry.get("timestamp"),
                "entidad": event.get("entidad"),
                "descripcion": f"Actualización en {event.get('rama')}",
                "estado": event.get("estado", "Vigente")
            })

        export = {
            "generated_at": datetime.utcnow().isoformat(),
            "source": "Magic Bank",
            "type": "student_summary",
            "items": summary
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export, f, indent=2, ensure_ascii=False)

        return output_path

    # ================================
    # EXPORTACIÓN INSTITUCIONAL
    # ================================
    def export_institutional(self, output_path: str):
        data = self._load_history()

        export = {
            "institution": "Magic Bank",
            "generated_at": datetime.utcnow().isoformat(),
            "description": "Historial institucional de actualizaciones académicas",
            "records": data.get("events", [])
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export, f, indent=2, ensure_ascii=False)

        return output_path
