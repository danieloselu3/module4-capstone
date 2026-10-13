"""Gold fixture checks: T-001..T-003 are fixed, and every fixture row's label must agree with
the router (the same comparison scripts/diagnose_fixture.py makes)."""
import json
from pathlib import Path

from agents.router import route

ROWS = [json.loads(line) for line in Path('fixtures/triage_messages_sample.jsonl').read_text().splitlines()
        if line.strip()]


def test_gold_rows_are_stable():
    by_id = {r['id']: r for r in ROWS}
    assert (by_id['T-001']['label'], by_id['T-002']['label'], by_id['T-003']['label']) == \
        ('triage', 'logistics_lookup', 'catalog_mismatch')


def test_every_fixture_row_agrees_with_the_router():
    bad = [(r['id'], r['text'], r['label'], route(r['text'])) for r in ROWS if route(r['text']) != r['label']]
    assert bad == [], f'{len(bad)} disagreeing rows, first: {bad[:3]}'
