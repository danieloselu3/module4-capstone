# Build checkpoint

## Works now
Each line has its evidence:
- **Path:** AfyaPlus Module 4 Capstone (`proposal.md`). Skill matrix complete for Weeks 1 to 10 (`skill_matrix.md`). `integration_map.json` lists 10 artefacts, all paths on disk (`check_integration_map.py`: OK 10).
- **One-command MWP in stub mode:** `python run_demo.py`. The transcript is in `evidence/demo_transcript.txt`. It covers auth (JWT 200/401), RAG-grounded triage (`faq-fever`, `faq-danger-signs`), MCP `check_stock` (C04 = 5 ORS units, reorder; `*` refused with 400), the Week 10 catalog lane (NK-99 flagged), RBAC 403, injection 400, pins and the eval score.
- **Tests:**
  - unit `pytest -q`: 45 passed
  - security smoke: 9 passed
  - integration: 4 passed + 1 live-port test (passes with `SERVICE_UP=1`)
  - perf: 2 passed
  - CI green on PRs #1 to #3 (ruff, every layer, eval gate, fixture diagnosis, pins)
- **Eval:** golden set 30/32 = 0.94, gate 0.90. The two misses are realistic phrasings the keyword router does not know ("ran out of amoxicillin", "picture on my product page"). Both fall back to triage, where a person reads them.
- **Perf:** `perf_stub.json` gives p95 = 0.025 s over 50 `/health` calls on a laptop. It is a teaching stub, not an SLA.
- **Fixtures:** 300 synthetic rows, and `diagnose_fixture.py` says all agree with the router. The catalog fixture is kept apart (test-enforced).
- **Security:** `.env` never tracked, no key or JWT in any ref's history, audit log carries no token, ID or phone (`evidence/audit_sample.jsonl`).

## Incident note
- **What broke:** the new gold-fixture test failed. 28 "where is my order" rows labelled `logistics_lookup` were routed to `triage` ([CI run 38450792523](https://github.com/danieloselu3/module4-capstone/actions/runs/38450792523), commit `4e5bca4`).
- **How we found it:** we read the failing assert, then `python scripts/diagnose_fixture.py` listed the same 28 ids. The label was right and `config.json` lacked a keyword.
- **The fix:** we added `"my order"` (not bare "order", which would misroute "eating disorder") plus two regression tests (commit `fc86f9e`). Details: [incidents/fixture_incident.md](incidents/fixture_incident.md).
- Also: the starter as shipped fails CI on `main` (commit `d2111a5`) because of its empty `pin.json`, `app.py` and `redact.py`, ruff errors, and no `setup-python`. That was fixed in PR #1.

## Deferred
- **Live LLM:** not wired. There is no key this week; `stub=False` raises `NotImplementedError`. Cost of ~10 live demo calls is estimated at ~$0.0004 in docs/cost_analysis.md.
- **Live cloud or Docker deploy:** steps are written in docs/deployment.md and marked "not executed live".
- **LLM agent loop over MCP:** the router calls `check_stock` in-process. The same tool serves over stdio, but no model chooses tools here (Week 7 had the LangChain agent).
- **Week 4 fine-tuned model:** referenced in the skill matrix, not served.
- **A classmate peer review:** declared solo self-review against the checklist on each PR (review_log.md).
- **Router quality:** keyword routing misses paraphrases (see the eval misses). A better router would be a classifier or an LLM with the golden set as its gate.
