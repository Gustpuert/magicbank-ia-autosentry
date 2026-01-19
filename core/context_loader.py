import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path("registry/history.json")


def load_authorized_context(area: str | None = None) -> str:
    """
    Devuelve el contexto oficial autorizado para los tutores IA.
    No interpreta, no modifica, no decide.
    """

    if not HISTORY_FILE.exists():
        return "No existen actualizaciones oficiales registradas."

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    events = data.get("events", [])

    if not events:
        return "No existen actualizaciones oficiales registradas."

    output = []
    output.append("ACTUALIZACIONES OFICIALES CONFIRMADAS")
    output.append(f"Fecha de generación: {datetime.utcnow().isoformat()} UTC\n")

    for entry in events:
        event = entry.get("event", {})

        if area and event.get("rama") != area:
            continue

        output.append(
            f"- País: {event.get('pais')}\n"
            f"  Entidad: {event.get('entidad')}\n"
            f"  Rama: {event.get('rama')}\n"
            f"  Fuente: {event.get('fuente')}\n"
        )

    if len(output) <= 2:
        return "No existen actualizaciones relevantes para esta área."

    return "\n".join(output)
