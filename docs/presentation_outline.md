# Presentation outline (10 slides for Week 12 Monday)

Rendered to `docs/presentation.pdf` by `python scripts/build_deck.py`. The talk script is in `docs/speaker_notes.md`.

1. **Problem and user.** AfyaPlus coordinators use three separate tools (triage, stock, listings), each with its own login and rules. The user is a clinic coordinator or a partner clinic. The decision supported is what to do next; people decide.
2. **Path chosen and why.** The official AfyaPlus Module 4 path. It reuses real Week 5 to 10 artefacts instead of a rewrite. Stub mode keeps it free and testable, and costs $0 this week.
3. **Architecture diagram with module boundaries.** One door: JWT, then guard, then router, then RBAC, then a tool (triage+RAG, MCP check_stock, catalog), then audit. Clinical and catalog fixtures stay in separate folders.
4. **Skill coverage.** The skill matrix rows, each pointing to a file. integration_map.json lists 10 artefacts from Weeks 5 to 10.
5. **Live demo.** `python run_demo.py`. The backup is `evidence/demo_transcript.txt`.
6. **Testing evidence.** 45 unit, 9 smoke, 4+1 integration, 2 perf. Eval 30/32 = 0.94 with a 0.90 gate. CI green. The fixture incident went red then green.
7. **Security and compliance choices.** JWT 401, injection 400 before any tool, RBAC 403, one-clinic allowlist, redact-then-hash audit, pins, no secrets in history, fixtures never mixed (Kenya DPA).
8. **Cost table with assumptions.** $0 this week. At 2,000 calls/day, about $2.23/month in tokens, or $0.89 with the cache. Tokens are about 1% of the all-in cost.
9. **What works vs deferred.** Works: the MWP end to end in stub mode. Deferred: the live LLM, cloud deploy, the agent loop, the Week 4 model and a classmate review.
10. **Process.** Three feature branches into three PRs, a self-review checklist on each, review_log.md. Next: a classifier router gated by the golden set, then the live key behind a flag.
