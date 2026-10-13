# Module 4 Capstone: AfyaPlus Health Ops

[![ci](https://github.com/danieloselu3/module4-capstone/actions/workflows/ci.yml/badge.svg)](https://github.com/danieloselu3/module4-capstone/actions/workflows/ci.yml)

## Overview
AfyaPlus Health Ops is one authenticated message API for clinic coordinators that integrates the Week 5 to 10 work into a single system. Each message to `POST /triage` passes:
1. JWT authentication
2. an injection guard
3. a keyword router
4. a role matrix

It then reaches one of three tools:
- **triage**: a stub model with a red-flag safety floor, grounded by RAG over the Week 5 knowledge base, with a pinned prompt and the Week 7 cache
- **logistics_lookup**: the MCP `check_stock` tool, one allowlisted clinic per call
- **catalog_mismatch**: the Week 10 SokoniHub scorer, with its own fixtures

Every call leaves a redacted, hashed audit line.

It runs entirely in **stub mode**: no API key, $0, and deterministic tests. One command (`python run_demo.py`) runs the whole flow. Path: the official AfyaPlus Module 4 path.

## Project path
- [x] AfyaPlus Module 4 Capstone (recommended)
- [ ] Domain / field alternative with skill checklist

Brief: [proposal.md](proposal.md). Skills: [skill_matrix.md](skill_matrix.md). Artefacts: [integration_map.json](integration_map.json) (10 rows, all paths checked).

## Week reuse (open these)
- **Weeks 1-5:**
  - The system prompt is a reviewed, pinned file (Weeks 1-3 prompt habits): [services/triage/prompts/](services/triage/prompts/).
  - RAG over the Week 5 `knowledge.json` (copied from afyaplus-multimodal-intake): [services/rag/](services/rag/).
  - The Week 4 golden-set and eval habit lives on in [evals/](evals/). The fine-tuned model itself is deferred.
- **Week 6:** FastAPI + JWT triage API (afyaplus-platform): [services/triage/app.py](services/triage/app.py), [auth.py](services/triage/auth.py).
- **Week 7:**
  - The MCP logistics tool: [agents/tools/logistics.py](agents/tools/logistics.py).
  - The exact-match response cache: [services/triage/model.py](services/triage/model.py).
  - Cost numbers: [docs/cost_analysis.md](docs/cost_analysis.md).
- **Week 8 (pins):** [services/triage/prompts/pin.json](services/triage/prompts/pin.json) carries the same prompt 1.2.0 sha `85e5cb1d…` as afyaplus-week8 and fails closed at boot. The knowledge corpus is pinned in [services/rag/knowledge/corpus_pin.json](services/rag/knowledge/corpus_pin.json).
- **Week 9 (smoke):**
  - [tests/test_security_smoke.py](tests/test_security_smoke.py).
  - Controls in [services/triage/security/](services/triage/security/) and [redact.py](services/triage/redact.py).
  - The one-clinic allowlist in `check_stock`.
- **Week 10 (catalog):** [services/catalog/](services/catalog/), the sokonihub-mm lab-bow-v1 scorer with its own fixture. It is never mixed with the clinical fixtures; [test_fixture_separation.py](tests/unit/test_fixture_separation.py) enforces this.

## Dataset
- [fixtures/](fixtures/): **300 synthetic rows** (200 to 500 allowed). No production scrape, no PII. See [fixtures/README.md](fixtures/README.md).
- [services/catalog/fixtures/](services/catalog/fixtures/): 10 SokoniHub listings, kept apart.
- [services/rag/knowledge/](services/rag/knowledge/): 7 teaching FAQ passages plus 24 Week 5 entries (19 used; the not-health items are dropped).

## Quick start
```bash
python -m venv venv && venv\Scripts\activate      # Python 3.12
pip install -r requirements.txt
pytest -q                                         # 45 passed (unit layer)
python run_demo.py                                # whole flow, writes evidence/demo_transcript.txt
```

## Docs
- [docs/architecture.md](docs/architecture.md): diagram, module and data boundaries
- [docs/deployment.md](docs/deployment.md): run, env vars, health; container and cloud steps "not executed live"
- [docs/cost_analysis.md](docs/cost_analysis.md): teaching table and assumptions
- [docs/user_guide.md](docs/user_guide.md): run steps, demo users, health and test commands, stub path
- [docs/build_checkpoint.md](docs/build_checkpoint.md): what works (with evidence), the incident, what is deferred
- Also: [docs/incidents/fixture_incident.md](docs/incidents/fixture_incident.md), [fixtures/README.md](fixtures/README.md)

## Testing
- **unit (default):** `pytest -q` gives **45 passed**: router plus gold cases, gold fixture checks, service functions in stub mode, MCP tool, pins and fixture separation.
- **integration:** `pytest -m integration` gives 4 passed via TestClient. `SERVICE_UP=1` also runs the live-port httpx `/health` test (passed locally).
- **perf:** `pytest -m perf` is a timing stub plus [perf_stub.json](perf_stub.json), measured by `scripts/measure_perf.py`: p95 0.025 s over 50 calls on a laptop, not an SLA.
- **security:** `pytest tests/test_security_smoke.py` gives **9 passed**: `.env` untracked, no live keys, no key or JWT in any ref's history, redaction, JWT 401, injection 400 before any tool, RBAC 403, and an audit log without token, ID or phone.
- **eval:** `python evals/run_eval.py evals/golden.jsonl --min 0.90` gives **30/32 = 0.94**. It is printed in every CI run, and both misses fall back to triage.
- **CI:** [.github/workflows/ci.yml](.github/workflows/ci.yml) runs ruff, every layer, the eval gate, fixture diagnosis, pins and RAG smoke, and all starter-pack gates.
- **Broken-fixture diagnosis:** a real incident, red then green in CI history ([docs/incidents/fixture_incident.md](docs/incidents/fixture_incident.md)).

## Demo
**One command:** `python run_demo.py`. It starts the service, then exercises health, login, RAG-grounded triage, MCP `check_stock`, the catalog lane and the 401/403/400 refusals. It prints the pins, eval, smoke and fixture size, and stops the service. Transcript: [evidence/demo_transcript.txt](evidence/demo_transcript.txt). Audit sample: [evidence/audit_sample.jsonl](evidence/audit_sample.jsonl).

Three commands by hand (full version in [docs/user_guide.md](docs/user_guide.md)):
```bash
uvicorn services.triage.app:app --host 127.0.0.1 --port 8080 &
curl 127.0.0.1:8080/health
curl -X POST 127.0.0.1:8080/triage -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' -d '{"text":"child has fever"}'
```
Get `$TOKEN` from `POST /token` with `mercy` / `logistics2026`.

## Presentation
[docs/presentation.pdf](docs/presentation.pdf): 10 slides, built by `python scripts/build_deck.py` from [docs/presentation_outline.md](docs/presentation_outline.md). Talk script: [docs/speaker_notes.md](docs/speaker_notes.md). Presented Week 12 Monday.

## Peer review
- [review_log.md](review_log.md) has entries for PR #1, #2 and #3: date, PR, reviewer and outcomes.
- The checklist is [docs/peer_review_checklist.md](docs/peer_review_checklist.md) (11 items), applied as a comment on each PR.
- Git flow: `feature/monday-brief-integration` → PR #1, `feature/tuesday-tests-security` → PR #2, `feature/thursday-docs-demo` → PR #3. Each was merged with a merge commit, so branch history stays visible.
- The only direct commit to `main` is the unmodified starter import. As shipped, it failed CI (empty stubs), which PR #1 fixed.

## Fallbacks declared
- [x] **no live OpenAI key (stub agent).** `triage-stub-v1` plus a deterministic router; responses carry the model id; `stub=False` raises rather than pretends. Spend: $0.
- [x] **no Docker (integration manual).** Integration runs through TestClient, plus a live-port httpx test with `SERVICE_UP=1`; no image was built this week.
- [x] **no cloud deploy executed (docs only).** [docs/deployment.md](docs/deployment.md) marks those steps "not executed live".
- [x] **solo reviewer (self-review with checklist).** There is no classmate review yet; each PR carries a self-review comment against the checklist.
- [x] **no LLM agent loop.** `check_stock` is a real FastMCP tool called in-process (stub mode). The Week 7 LangChain agent is not re-wired.

## Submission checklist
- [x] proposal + skill_matrix + map (`check_proposal.py`, `check_integration_map.py` pass)
- [x] five docs linked (`check_doc_links.py` passes)
- [x] peer review completed (declared solo self-review on PRs #1-#3; `check_review_doc.py` passes)
- [x] slides PDF in docs/ and demo command documented
- [x] no secrets, no live PII crawls, no mixed clinical and catalog fixtures (tested)
