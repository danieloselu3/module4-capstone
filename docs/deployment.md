# Deployment

## Run locally
```bash
python -m venv venv && venv\Scripts\activate        # Python 3.12
pip install -r requirements.txt
uvicorn services.triage.app:app --host 127.0.0.1 --port 8080
```
Or run everything, from start to stop, with one command: `python run_demo.py`. It starts the service, exercises it, and stops it again.

Use `127.0.0.1` rather than `localhost` on Windows. `localhost` tries IPv6 first and adds about 2 s to each call (found while measuring `perf_stub.json`).

## Env vars
| Name | Needed | Notes |
|---|---|---|
| `JWT_SECRET` | yes in production | Signs tokens. With `APP_ENV=production` the service refuses to boot without it. In development a dev-only default is used with a warning. Never committed: `.env` is gitignored and the smoke test checks it. |
| `APP_ENV` | optional | `production` turns on the fail-closed boot |
| `LOG_DIR` | optional | Where `audit.jsonl` goes (default `logs/`, gitignored) |
| `OPENAI_API_KEY` | not used | Stub mode is the only path wired in this capstone (README fallbacks). A missing key changes nothing. |

## Health
`GET /health` returns 200 with the pins: `prompt_version`, `prompt_sha256`, `model_id`, `knowledge_docs`. Measured p95 is 0.025 s over 50 calls on a laptop (`perf_stub.json`). This is not an SLA.

## Container and cloud: not executed live
These steps are the plan only. No Docker image or cloud deploy was run for this capstone.
1. Build a `python:3.12-slim` image that runs as a non-root user and has no secrets in its layers (the Week 6 Dockerfile pattern).
2. Inject `JWT_SECRET` at run time (`--env-file`, or a Key Vault or KMS reference as in Week 9 `secret_refs.yaml`). The container must exit 1 if it is missing.
3. CI builds and tags `module4-capstone:<release>-<sha>`, never `latest`, and promotes the same digest from staging to production (the Week 8 pipeline).
4. Mount `LOG_DIR` on an encrypted volume and apply the 180-day audit retention (Week 9).

**Not executed live:** steps 1 to 4. No cloud credentials are used this week. Fallback declared in the README.
