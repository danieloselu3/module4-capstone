<!-- Change for your project: nothing required. Row count and rules stay generic. -->
# Fixtures

Teaching fixture target: 200 to 500 rows (about 300 for the default triage sample).
No production scrape. No mixed clinical and marketplace records in the same file.
Generate with: python scripts/make_fixture.py --rows 300 --out fixtures/triage_messages_sample.jsonl
Expand-to-~300-rows notes live here, in prose, not as a comment line inside the JSONL file itself.
