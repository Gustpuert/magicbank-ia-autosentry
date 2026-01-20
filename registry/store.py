import json
from pathlib import Path
from datetime import datetime

REGISTRY_FILE = Path("registry/events.json")


def _load():
    if not REGISTRY_FILE.exists():
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REGISTRY_FILE, "w") as f:
            json.dump({"events": []}, f, indent=2)

    with open(REGISTRY_FILE, "r") as f:
        return json.load(f)


def _save(data):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def store_event(event):
    data = _load()
    data["events"].append(event.to_dict())
    _save(data)


def store_if_changed(event):
    """
    Guarda el evento SOLO si no existe previamente.
    Evita duplicados.
    Es la función que el scheduler espera.
    """

    data = _load()
    events = data.get("events", [])

    fingerprint = (
        event.get("pais"),
        event.get("rama"),
        event.get("entidad"),
        event.get("fuente"),
    )

    for e in events:
        if (
            e.get("pais"),
            e.get("rama"),
            e.get("entidad"),
            e.get("fuente"),
        ) == fingerprint:
            return False  # Ya existe → no se guarda

    event["timestamp"] = datetime.utcnow().isoformat()
    events.append(event)
    data["events"] = events
    _save(data)

    return True
