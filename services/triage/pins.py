"""Week 8 pin: the system prompt is a file, and pin.json records its sha256 and the model id.

load_pinned_prompt() fails closed: an edited prompt file stops the service at import.
"""
import hashlib
import json
from pathlib import Path

PROMPTS = Path(__file__).resolve().parent / 'prompts'
PIN_PATH = PROMPTS / 'pin.json'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_pin() -> dict:
    return json.loads(PIN_PATH.read_text(encoding='utf-8'))


def load_pinned_prompt() -> tuple[dict, str]:
    pin = load_pin()
    path = PROMPTS / pin['prompt_file']
    got = sha256(path)
    if got != pin['sha256']:
        raise RuntimeError(f"PROMPT PIN MISMATCH {pin['prompt_file']}: {got[:12]} != {pin['sha256'][:12]}")
    return pin, path.read_text(encoding='utf-8')


if __name__ == '__main__':
    pin, text = load_pinned_prompt()
    print('prompt pin OK', pin['prompt_version'], pin['model_id'], pin['sha256'][:12], len(text), 'chars')
