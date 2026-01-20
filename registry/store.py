import json
from pathlib import Path
from datetime import datetime
import hashlib

REGISTRY_FILE = Path("registry/events.json")


def _hash_event(event: dict) -> str:
    """Genera un hash único del evento para evitar duplicados"""
    raw = json.dumps(event, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def store_if_changed(event: dict) -> bool:
    """
    Guarda el evento solo si es nuevo.
    Retorna True si fue almacenado, False si ya existía.
    """

    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "w") as f:
            json.dump({"events": []}, f, indent=2)

    with open(REGISTRY_FILE, "r") as f:
        data = json.load(f)

    event_hash = _hash_event(event)

    for e in data["events"]:
        if e.get("hash") == event_hash:
            return False  # Ya existe

    event["hash"] = event_hash
    event["stored_at"] = datetime.utcnow().isoformat()

    data["events"].append(event)

    with open(REGISTRY_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return True
