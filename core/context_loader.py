import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path("registry/history.json")


def load_authorized_context(area: str | None = None) -> str:
    """
    Devuelve el contexto autorizado para los tutores IA.

    - Lee el historial validado
    - Filtra por área si se indica
    - Devuelve texto limpio y usable
    """

    if not HISTORY_FILE.exists():
        return "No existen actualizaciones oficiales registradas."

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    events = data.get("events", [])

    if not events:
        return "No hay actualizaciones oficiales registradas."

    lines = []
    lines.append("ACTUALIZACIONES OFICIALES CONFIRMADAS\n")
    lines.append(f"Generado: {datetime.utcnow().isoformat()} UTC\n")

    for entry in events:
        event = entry.get("event", {})

        if area and event.get("rama") != area:
            continue

        lines.append(
            f"- [{event.get('pais')}] "
            f"{event.get('entidad')} | "
            f"{event.get('rama')} | "
            f"{event.get('fuente')}"
        )

    if len(lines) <= 2:
        return "No hay actualizaciones relevantes para esta área."

    return "\n".join(lines)
