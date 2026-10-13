"""Structured audit trail, one JSON object per line in $LOG_DIR/audit.jsonl (Week 9).

actor/role/action/resource/outcome stay readable; the payload is redacted then hashed.
Health text (accepted triage messages) is kept as a hash only.
"""
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

from services.triage.redact import redact_then_hash

_lock = threading.Lock()


def log_path() -> Path:
    return Path(os.getenv('LOG_DIR', 'logs')) / 'audit.jsonl'


def record(*, actor: str, role: str, action: str, resource: str, outcome: str,
           trace_id: str = '-', payload: str = '', keep_text: bool = True) -> dict:
    cleaned, digest = redact_then_hash(payload)
    row = {'ts': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'trace_id': trace_id,
           'actor': actor, 'role': role, 'action': action, 'resource': resource, 'outcome': outcome,
           'payload_sha': digest, 'payload_redacted': cleaned[:300] if keep_text else None}
    path = log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(row) + '\n')
    return row
