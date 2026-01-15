import json
from pathlib import Path

REGISTRY_FILE = Path("registry/events.json")

def store_event(event):
    if not REGISTRY_FILE.exists():
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REGISTRY_FILE, "w") as f:
            json.dump({"events": []}, f, indent=2)

    with open(REGISTRY_FILE, "r") as f:
        data = json.load(f)

    data["events"].append(event.to_dict())

    with open(REGISTRY_FILE, "w") as f:
        json.dump(data, f, indent=2)