import json
from pathlib import Path
from datetime import datetime

REGISTRY_FILE = Path("registry/history.json")


def store_if_changed(events: list) -> bool:
    """
    Guarda los eventos SOLO si hay cambios nuevos.
    Devuelve True si hubo cambios, False si no.
    """

    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Si no existe, crear archivo base
    if not REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "w") as f:
            json.dump({"events": []}, f, indent=2)

    with open(REGISTRY_FILE, "r") as f:
        data = json.load(f)

    previous_events = data.get("events", [])

    # Comparación simple: contenido exacto
    if events == previous_events:
        return False

    data["events"] = events
    data["last_update"] = datetime.utcnow().isoformat()

    with open(REGISTRY_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return True
