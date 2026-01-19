import json
from pathlib import Path
from datetime import datetime

REGISTRY_FILE = Path("registry/history.json")


def _init():
    if not REGISTRY_FILE.exists():
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
            json.dump({"events": []}, f, indent=2)


def load_history():
    _init()
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_event(event: dict):
    data = load_history()

    data["events"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "event": event
    })

    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
