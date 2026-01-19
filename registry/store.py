import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path("registry/history.json")


def _init_registry():
    if not HISTORY_FILE.exists():
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"events": []}, f, indent=2)


def load_history():
    _init_registry()
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def has_changes(new_events):
    history = load_history()
    previous = history.get("events", [])

    # Convertir a set para comparación real
    previous_set = {json.dumps(e, sort_keys=True) for e in previous}
    current_set = {json.dumps(e, sort_keys=True) for e in new_events}

    return current_set != previous_set


def store_if_changed(new_events):
    if not new_events:
        return False

    if not has_changes(new_events):
        return False

    data = {
        "last_update": datetime.utcnow().isoformat(),
        "events": new_events
    }

    save_history(data)
    return True
