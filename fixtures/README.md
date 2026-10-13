# Fixtures

**`triage_messages_sample.jsonl`: 300 rows**, inside the 200 to 500 teaching target. Every row is synthetic and shaped `{"id", "text", "label"}`, with labels `triage`, `logistics_lookup` or `catalog_mismatch`. Rows are short intent phrases only: no names, phone numbers, IDs, locations or real patient text.

Rules:
- **No production scrape.** Nothing here came from a live system or a crawl.
- **No millions of rows.** The fixture stays in the hundreds so tests are fast and reviewable.
- **No mixed clinical and marketplace records in the same file.** SokoniHub listings (Week 10) live only in `services/catalog/fixtures/sokonihub_catalog.json`. `tests/unit/test_fixture_separation.py` enforces both directions.
- Valid JSONL only: no comment lines inside the file. Notes like this one live here, in prose.

Generate with:
```bash
python scripts/make_fixture.py --rows 300 --out fixtures/triage_messages_sample.jsonl
```
This is deterministic (`random.seed(11)`). The gold rows T-001 to T-003 are fixed and tested in `tests/unit/test_fixture_routes.py`.

Check with:
```bash
python scripts/diagnose_fixture.py fixtures/triage_messages_sample.jsonl
```
Every row's label must agree with the router. That check found the Tuesday incident (docs/incidents/fixture_incident.md).
