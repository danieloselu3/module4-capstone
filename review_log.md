# Review log

Reviewer for every entry: **danieloselu3 (author), declared solo self-review** against docs/peer_review_checklist.md. No classmate review has happened yet; this is the brief's "solo cohort" fallback. The full review comment is on each PR.

| Date | PR | Reviewer | Outcome |
|---|---|---|---|
| 2026-10-13 | [#1](https://github.com/danieloselu3/module4-capstone/pull/1) Monday: brief, matrix, map + Weeks 5-10 integration | danieloselu3 (solo, self-review) | 6/8 ticked. Follow-ups: fixture diagnosis reported 28 disagreeing rows (carried to Tuesday); README docs links (carried to Thursday). Ask answered: partner_clinic may not use the triage tool (RBAC 403). Merged. |
| 2026-10-13 | [#2](https://github.com/danieloselu3/module4-capstone/pull/2) Tuesday: test pyramid, security smoke, eval gate, perf, fixture incident | danieloselu3 (solo, self-review) | 7/8 ticked. The fixture follow-up from #1 was **closed**: router fixed with "my order", not bare "order" (it would misroute "eating disorder"); CI red run 38450792523 then green. Nit: the starter's httpx test uses `localhost` (about 2 s on Windows), left as shipped. Docs carried to Thursday. Merged. |
| 2026-10-13 | [#3](https://github.com/danieloselu3/module4-capstone/pull/3) Thursday: docs pack, one-command demo, deck, review | danieloselu3 (solo, self-review) | 11/11 ticked. The docs follow-up from #1 and #2 was **closed**: README links all five docs and `check_doc_links.py` passes. Nit: the deck numbers are copied from build_checkpoint.md, so rebuild `scripts/build_deck.py` if they change. Merged. |
