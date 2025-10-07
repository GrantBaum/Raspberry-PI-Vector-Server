# vector_brain.py
import os
import re
from datetime import datetime

# import requests # Uncomment if you want to actually call wire-pod

WIREPOD_URL = os.getenv("WIREPOD_URL", "http://127.0.0.1:8080")
DRY_RUN = os.getenv("BRAIN_DRY_RUN", "1") == "1" # keep off-network by default

def normalize(text: str) -> str:
    t = text.strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t

def detect_intent(text: str) -> dict:

    ## Returns a dict describing what to do and (optionally) what to say back.
    ## { "intent": "...", "params": {...}, "say": "..." }

    t = normalize(text)

    # Greetings
    if any(k in t for k in ["hello", "hi vector", "hey vector", "hey there"]):
        return {"intent": "say", "params": {"text": "Hello!"},
        "say": "Hello!"}

    # Come here
    if "come here" in t or "come to me" in t:
        return {"intent": "move", "params": {"cmd": "come_here"},
        "say": "On my way."}

    # Dance
    if "dance" in t:
        return {"intent": "animation", "params": {"name": "dance"},
        "say": "Let me show you some moves."}

    # Battery/status
    if "battery" in t or "status" in t:
    # Placeholder; normally query wire-pod then speak result
        return {"intent": "status_battery", "params": {},
        "say": "Checking my battery."}

    # Time
    if "time" in t:
        now = datetime.now().strftime("%-I:%M %p") if os.name != "nt" else datetime.now().strftime("%I:%M %p").lstrip("0")
        return {"intent": "say", "params": {"text": f"The time is {now}."},
        "say": f"The time is {now}."}

    # Fallback
    return {"intent": "none", "params": {}, "say": "Sorry, I didn't catch that."}

def act(action: dict) -> dict:

## Optionally send the action to Vector via wire-pod.
## For now, this is a no-op (returns what would happen).
## Uncomment requests and wire-pod calls when you’re ready.

    intent = action.get("intent")
    params = action.get("params", {})

    if DRY_RUN or intent == "none":
        return {"ok": True, "sent": False, "intent": intent, "params": params}

# Example mappings — replace with your actual wire-pod endpoints
# try:
# if intent == "say":
# r = requests.post(f"{WIREPOD_URL}/vector/say", json=params, timeout=2)
# return {"ok": r.ok, "status": r.status_code}
# if intent == "move":
# r = requests.post(f"{WIREPOD_URL}/vector/move", json=params, timeout=2)
# return {"ok": r.ok, "status": r.status_code}
# if intent == "animation":
# r = requests.post(f"{WIREPOD_URL}/vector/animation", json=params, timeout=2)
# return {"ok": r.ok, "status": r.status_code}
# if intent == "status_battery":
# r = requests.get(f"{WIREPOD_URL}/vector/status/battery", timeout=2)
# return {"ok": r.ok, "status": r.status_code, "data": r.json()}
# except Exception as e:
# return {"ok": False, "error": str(e)}

    return {"ok": True, "sent": False, "intent": intent, "params": params}


