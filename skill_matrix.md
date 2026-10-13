# Skill coverage matrix

| Skill | Week resource to open | My module / file | Required / Optional |
| --- | --- | --- | --- |
| LLM fundamentals: system prompt as a reviewed file | Weeks 1-3 prompt labs; Week 8 `prompts/triage_system_v1.2.0.txt` | services/triage/prompts/triage_system_v1.2.0.txt | Required |
| Fine-tune / eval habit | Week 4 afyaplus-llama-finetune (golden set + judge idea) | evals/golden.jsonl, evals/run_eval.py (stub router eval, no fine-tune re-run) | Optional |
| RAG / grounded lookup | Week 5 afyaplus-multimodal-intake `knowledge.json` | services/rag/retriever.py, services/rag/knowledge/ | Required |
| API or agent path | Week 6 triage API lab (afyaplus-platform: FastAPI + JWT) | services/triage/app.py, services/triage/auth.py | Required |
| Cost / MCP tools | Week 7 MCP logistics + response cache (afyaplus-week7) | agents/tools/logistics.py, services/triage/model.py (cache), docs/cost_analysis.md | Required |
| Pin / versioning | Week 8 pin.json (afyaplus-week8) | services/triage/prompts/pin.json, services/triage/pins.py, services/rag/knowledge/corpus_pin.json | Required |
| Security hygiene | Week 9 security smoke (afyaplus-week9) | tests/test_security_smoke.py, services/triage/security/, services/triage/redact.py | Required |
| Eval / test | Week 11 Tuesday pyramid + golden set | tests/unit/, tests/integration/, tests/perf/, evals/golden.jsonl | Required |
| Docs | Prior READMEs + Week 11 docs | docs/ (five docs), fixtures/README.md, README.md | Required |
| Optional multimodal | Week 10 catalog (sokonihub-mm) | services/catalog/ (own fixtures, never mixed) | Optional |
