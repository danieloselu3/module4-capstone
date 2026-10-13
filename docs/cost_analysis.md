# Cost analysis

Teaching table. Prices are gpt-4o-mini list prices as used in Week 7: $0.15 per 1M input tokens and $0.60 per 1M output tokens (OpenAI pricing page; re-check before quoting). Token shape is the Week 7 measurement: 123 prompt and 31 completion tokens per triage call, so one live call costs 123 × 0.15/1M + 31 × 0.60/1M = **$0.0000371**.

| Call type | Calls (n) | Unit cost | Total | Assumptions |
| --- | --- | --- | --- | --- |
| Stub tests (unit, smoke, integration, perf) | 0 live | $0 | $0 | CI never calls a live key; `triage-stub-v1` is deterministic |
| Golden-set eval (32 rows, router) | 0 live | $0 | $0 | The eval scores the router, which is keyword-based and free |
| One-command demo (`run_demo.py`) | 0 live | $0 | $0 | Stub mode only; this is what was run this week |
| Thursday demo if a live key were wired | ~10 | $0.0000371 | ~$0.0004 | Budget cap is about $1; actual spend this week was $0 |
| Production estimate, 2,000 triage/day | 60,000 / month | $0.0000371 | ~$2.23 / month | Week 7 baseline volume; no cache |
| Same, with Week 7 cache (hit rate 0.60) | 24,000 billed / month | $0.0000371 | ~$0.89 / month | Week 7 measured 0.60 hits on its fixture; real traffic may differ |
| MCP `check_stock`, RAG retrieval, catalog scorer | any | $0 tokens | $0 | Run in-process, with no model call |

## Assumptions and what dominates
- Tokens are small change. Week 7 found the all-in cost was about $3.11 per 1k requests, about 1% of it tokens. People and the container dominate, and this table leaves both out.
- The cache key includes the prompt sha, so a prompt change never serves old answers and the hit rate resets on a new prompt.
- Live calls would go through a client with `max_retries=1` (Week 7 retry-storm lesson).
- Spend this week: **$0**. No key was used. Any live demo stays under the brief's ~$1 cap.
