"""Tool names and keywords come from config.json (starter pack). Adapted only to read
config.json next to the repo root, so the router works from any working directory."""
import json
from pathlib import Path

CONFIG = json.loads((Path(__file__).resolve().parent.parent / "config.json").read_text())
TOOLS = CONFIG["tools"]
KEYWORDS = CONFIG["route_keywords"]


def route(intent: str) -> str:
    t = intent.lower()
    for tool, words in KEYWORDS.items():
        if any(w in t for w in words):
            return tool
    return TOOLS[0]
