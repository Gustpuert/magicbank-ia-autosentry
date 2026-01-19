import json
from pathlib import Path
from datetime import datetime

# Archivo de histórico
REGISTRY_FILE = Path("registry/history.json")


def _init_registry():
    """Crea el archivo de historial si no existe"""
    if not REGISTRY_FILE.exists():
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "metadata": {
                        "created_at": datetime.utcnow().isoformat(),
                        "system": "MagicBank IA AutoSentry",
                        "version": "1.0"
                    },
                    "events": []
                },
                f,
                indent=2,
                ensure_ascii=False
            )


def store_event(event):
    """
    Guarda un evento detectado por cualquier detector.
    El evento debe exponer un método to_dict()
    """
    _init_registry()

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event.to_dict()
    }

    data["events"].append(record)

    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
