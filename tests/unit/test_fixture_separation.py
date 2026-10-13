"""No clinical rows in catalog fixtures, no marketplace rows in clinical fixtures, and the
clinical fixture stays in the hundreds."""
import json
from pathlib import Path

CLINICAL = Path('fixtures/triage_messages_sample.jsonl')
CATALOG = Path('services/catalog/fixtures/sokonihub_catalog.json')
MARKET_FIELDS = {'sku', 'image', 'image_tags', 'title', 'description', 'category'}
CLINICAL_FIELDS = {'text', 'label', 'patient_message', 'urgency', 'county', 'symptoms'}


def clinical_rows():
    return [json.loads(line) for line in CLINICAL.read_text(encoding='utf-8').splitlines() if line.strip()]


def test_clinical_fixture_is_in_the_hundreds_and_clean_jsonl():
    rows = clinical_rows()
    assert 200 <= len(rows) <= 500
    assert all(set(r) == {'id', 'text', 'label'} for r in rows)


def test_no_marketplace_fields_in_clinical_fixture():
    assert not any(MARKET_FIELDS & set(r) for r in clinical_rows())


def test_no_clinical_fields_in_catalog_fixture():
    rows = json.loads(CATALOG.read_text(encoding='utf-8'))
    assert rows and not any(CLINICAL_FIELDS & set(r) for r in rows)


def test_catalog_fixture_lives_only_under_services_catalog():
    assert not list(Path('fixtures').glob('*catalog*')) and not list(Path('fixtures').glob('*sokoni*'))
