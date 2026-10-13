"""Change for your project: nothing. Adapt only if your repo layout differs."""
import re
import subprocess
from pathlib import Path

_LIVE_KEY = re.compile(r"sk-live-[A-Za-z0-9_-]{6,}")


def test_env_not_tracked():
    out = subprocess.check_output(['git', 'ls-files'], text=True)
    assert '.env' not in out.splitlines()


def test_no_sample_live_key_in_repo():
    for p in Path('.').rglob('*.py'):
        if 'venv' in p.parts or 'tests' in p.parts:
            continue
        assert _LIVE_KEY.search(p.read_text()) is None, f'live-looking key in {p}'


def test_redaction_strips_email():
    from services.triage.redact import redact
    assert 'user@example.com' not in redact('contact user@example.com now')
