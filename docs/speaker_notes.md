# Speaker notes (Week 12 Monday: 7 min talk + 3 min demo + 3 min questions)

Timing: about 40 seconds a slide for slides 1 to 4 and 6 to 10, which gives about 6.5 minutes. Slide 5 is the 3-minute demo.

**1. Problem and user (0:00).** "A coordinator at a western Kenya clinic has three tools from this module: triage, a stock lookup and a listing checker. Each has its own login and its own rules. I built one door in front of all three. The system recommends; the coordinator decides."

**2. Path (0:40).** "I took the official AfyaPlus path. Everything you'll see is real code from Weeks 5 to 10, copied in and wired together, not rewritten. It runs in stub mode: no API key, $0, and every test is deterministic."

**3. Architecture (1:20).** Point left to right. "Every message hits the same door. First a JWT check, then the injection guard, which refuses instruction-like text before anything runs. Then the router picks one of three tools, the role matrix decides whether you may use it, and one redacted audit line is written. The clinical fixtures and the SokoniHub listings live in separate folders, and a test enforces it."

**4. Skill coverage (2:00).** "Each required skill maps to a week and a file: the API from Week 6, the MCP tool and cache from Week 7, the pins from Week 8, security from Week 9, and the catalog lane from Week 10. The integration map lists ten artefacts, and a checker proves the paths exist."

**5. Live demo (2:40, 3 minutes).** Run `python run_demo.py` and narrate as it prints:
- health: "the pinned prompt hash, the same as Week 8"
- fever: "medium urgency, grounded in the fever FAQ, with sources"
- chest pain: "the red-flag floor makes it high"
- ORS at C04: "the MCP tool returns 5 units and says reorder"
- star: "a wildcard is refused, so there's no bulk dump"
- NK-99: "the Week 10 lane flags the mismatch"
- refusals: "no token gets 401, a partner asking for triage gets 403, the injection gets 400"
- the eval score and smoke results at the end
**Backup if it fails:** open `evidence/demo_transcript.txt` and walk through the same lines. Say that it is the recorded run.

**6. Testing (5:40).** "There are 45 unit tests, 9 security smoke tests, and integration and perf layers behind markers, all green in CI. The eval is 30 of 32. I added the two misses on purpose: paraphrases a keyword router can't read. Both fall back to triage, the safe side. On Tuesday a new fixture test went red on 28 rows. The labels were right and the router was missing a keyword. I fixed the router, not the test."

**7. Security (6:20).** "Week 9 carried over. Authentication is not authorisation. A one-clinic allowlist means no bulk export, and the audit log is redacted before it is written. Health text is kept as a hash only. There are no secrets in git history, and a test checks that."

**8. Cost (7:00).** "This week cost nothing. With a live model at 2,000 messages a day, tokens are about two dollars a month, under one with the Week 7 cache. Tokens are about 1% of the real cost; people and hosting dominate."

**9. Works vs deferred (7:40).** "It works end to end in stub mode. I did not wire the live model, the cloud deploy or an agent loop, and I'll say so rather than claim them."

**10. Process (8:20).** "Three feature branches and three PRs, each reviewed against the checklist. I reviewed solo and declared it. Next: replace the keyword router with a classifier, using the golden set as its gate."

**Likely questions**
- *Why stub mode?* It is deterministic tests at $0. The live path is one flag away, and the docs say it is not wired.
- *What stops a partner reading every clinic's stock?* The allowlist plus one clinic per call, and the tool re-checks the role itself.
- *Is the catalog data safe beside patient data?* It's not beside it: there are separate folders and a test that fails if they mix.
