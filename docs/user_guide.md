# User guide

## Run
One command does everything (start, exercise, stop, transcript):
```bash
python run_demo.py            # writes evidence/demo_transcript.txt
```
Or run the service yourself (see docs/deployment.md):
```bash
uvicorn services.triage.app:app --host 127.0.0.1 --port 8080
```

## Demo users (bcrypt hashes in services/triage/auth.py)
| User | Password | Role | May use |
|---|---|---|---|
| mercy | logistics2026 | clinical_ops | triage, stock look-ups, catalog checks |
| guest | viewonly2026 | partner_clinic | stock look-ups only |

## Three-command demo
```bash
# 1. start the service
uvicorn services.triage.app:app --host 127.0.0.1 --port 8080 &
# 2. confirm health (shows the pinned prompt and model id)
curl 127.0.0.1:8080/health
# 3. log in, then send one message
TOKEN=$(curl -s -X POST 127.0.0.1:8080/token -H 'Content-Type: application/json' \
  -d '{"username":"mercy","password":"logistics2026"}' | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
curl -X POST 127.0.0.1:8080/triage -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"text":"My child has had a fever since yesterday"}'
```
What you can send to `/triage`:
- Symptoms such as "chest pain and dizziness" return an urgency, advice and grounded guidance with source ids.
- "How much ORS stock is at C04?" calls the MCP `check_stock` tool for one clinic. `*` is refused.
- "Check the listing photo for NK-99" runs the Week 10 catalog scorer.

## Health and test commands
```bash
curl 127.0.0.1:8080/health
pytest -q                                       # unit layer (default)
pytest tests/test_security_smoke.py -q          # Week 9 security smoke
pytest -q -m integration                        # HTTP flow (SERVICE_UP=1 also runs the live-port test)
pytest -q -m perf                               # timing stub + perf_stub.json check
python evals/run_eval.py evals/golden.jsonl --min 0.90
python scripts/measure_perf.py --url http://127.0.0.1:8080/health --n 50 --out perf_stub.json
python scripts/diagnose_fixture.py fixtures/triage_messages_sample.jsonl
```

## Fallback path
Stub mode is the default and the only wired path:
- The triage model is `triage-stub-v1`, a keyword urgency with a red-flag floor. It never prescribes.
- The answer quotes retrieved guidance only and says so when nothing matches.
- `check_stock` runs in-process.

No API key is read, and `handle_message(..., stub=False)` raises `NotImplementedError` rather than pretending. Responses always carry `model_id: triage-stub-v1`, so a stub answer is never mistaken for a live model.

## Fixture location
`fixtures/triage_messages_sample.jsonl` holds 300 synthetic rows (200 to 500 allowed); see fixtures/README.md. Catalog listings live separately in `services/catalog/fixtures/`.
