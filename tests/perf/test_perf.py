"""Perf layer (pytest -m perf): timing stub only. perf_stub.json itself is written by
scripts/measure_perf.py against the running service (never hand-edited)."""
import json
import time
from pathlib import Path

import pytest

from services.triage.app import handle_message

pytestmark = pytest.mark.perf


def test_stub_handle_message_p95_under_50ms():
    samples = []
    for i in range(50):
        start = time.perf_counter()
        handle_message({'text': f'fever day {i}'})          # unique text: every call is a cache MISS
        samples.append(time.perf_counter() - start)
    samples.sort()
    assert samples[int(len(samples) * 0.95) - 1] < 0.05


def test_measured_perf_stub_is_committed_and_captioned():
    data = json.loads(Path('perf_stub.json').read_text(encoding='utf-8'))
    assert data['n_samples'] >= 10 and data['p95_seconds'] > 0
    assert 'not a production SLA' in data['caption']
