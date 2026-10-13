"""Change for your project: nothing. Tool names and keywords come from config.json."""
import json
from pathlib import Path

CONFIG = json.loads(Path("config.json").read_text())
TOOLS = CONFIG["tools"]
KEYWORDS = CONFIG["route_keywords"]


def route(intent: str) -> str:
    t = intent.lower()
    for tool, words in KEYWORDS.items():
        if any(w in t for w in words):
            return tool
    return TOOLS[0]
