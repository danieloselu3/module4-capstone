# Incident: 28 fixture rows disagreed with the router (Tuesday diagnosis drill)

**What broke.** The new gold-fixture test `tests/unit/test_fixture_routes.py` failed on commit `4e5bca4`. Of the 300 rows in `fixtures/triage_messages_sample.jsonl`, 28 ("where is my order", labelled `logistics_lookup`) were routed to `triage`. CI went red: [run 38450792523](https://github.com/danieloselu3/module4-capstone/actions/runs/38450792523).

**How we found it.** We read the failing assert, then confirmed with `python scripts/diagnose_fixture.py fixtures/triage_messages_sample.jsonl`, which listed T-004, T-016, T-025 and 25 more, all with the same text. The **label was right**, because a missing order is a logistics question. The **router was wrong**: `config.json` had no keyword that matches "where is my order".

**The fix.** We added `"my order"` (not bare `"order"`) to `route_keywords.logistics_lookup` in `config.json`. Bare "order" would have sent clinical text such as "eating disorder" away from triage, which is the wrong direction for a health system. Two regression tests now pin both cases (`tests/unit/test_router.py`). Neither the test nor the fixture was deleted or edited to silence the failure.

Failing output (before the fix):
```
$ pytest -q tests/unit/test_fixture_routes.py
E  AssertionError: 28 disagreeing rows, first: [('T-004', 'where is my order', 'logistics_lookup', 'triage'), ('T-016', 'where is my order', 'logistics_lookup', 'triage'), ('T-025', 'where is my order', 'logistics_lookup', 'triage')]
1 failed, 1 passed

$ python scripts/diagnose_fixture.py fixtures/triage_messages_sample.jsonl
FAIL disagreements: [('T-004', 'logistics_lookup', 'triage'), ('T-016', 'logistics_lookup', 'triage'), ('T-025', 'logistics_lookup', 'triage'), ...]   (exit 1)
```
After the fix:
```
$ python scripts/diagnose_fixture.py fixtures/triage_messages_sample.jsonl
diagnose OK, all rows agree with router
```
