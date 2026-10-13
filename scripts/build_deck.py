#!/usr/bin/env python3
"""Build docs/presentation.pdf (10 slides, 16:9) from the filled docs/presentation_outline.md.

    python scripts/build_deck.py

reportlab only (the Week 7 one-pager tool). Numbers on the slides are the ones in
docs/build_checkpoint.md; re-run after they change.
"""
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'docs' / 'presentation.pdf'
W, H = 960, 540
INK, MUTED, ACCENT, SOFT, LINE = HexColor('#1f2933'), HexColor('#52606d'), HexColor('#0b6e69'), \
    HexColor('#e6f2f1'), HexColor('#c7d2d9')


def header(c, n, title, kicker=''):
    c.setFillColor(white)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(ACCENT)
    c.rect(0, H - 6, W, 6, stroke=0, fill=1)
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 11)
    c.drawString(48, H - 40, kicker or 'AfyaPlus Health Ops - Module 4 capstone')
    c.drawRightString(W - 48, H - 40, f'{n} / 10')
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 30)
    c.drawString(48, H - 86, title)


def bullets(c, items, x=48, y=H - 140, size=17, gap=34, width=860):
    c.setFont('Helvetica', size)
    for item in items:
        sub = item.startswith('  ')
        text = item.strip()
        c.setFillColor(MUTED if sub else ACCENT)
        c.circle(x + (28 if sub else 6), y + 5, 3 if sub else 4, stroke=0, fill=1)
        c.setFillColor(INK if not sub else MUTED)
        c.setFont('Helvetica', size - (2 if sub else 0))
        for i, line in enumerate(wrap(text, size, width - (40 if sub else 20))):
            c.drawString(x + (40 if sub else 20), y - i * (size + 4), line)
        y -= gap + (len(wrap(text, size, width)) - 1) * (size + 4)
    return y


def wrap(text, size, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if len(trial) * size * 0.5 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    return lines + [cur]


def box(c, x, y, w, h, title, sub='', fill=SOFT):
    c.setFillColor(fill)
    c.setStrokeColor(ACCENT)
    c.roundRect(x, y, w, h, 8, stroke=1, fill=1)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 13)
    c.drawCentredString(x + w / 2, y + h - 22, title)
    c.setFont('Helvetica', 10.5)
    c.setFillColor(MUTED)
    for i, line in enumerate(sub.split('\n')):
        c.drawCentredString(x + w / 2, y + h - 40 - i * 14, line)


def arrow(c, x1, y1, x2, y2):
    c.setStrokeColor(MUTED)
    c.setLineWidth(1.5)
    c.line(x1, y1, x2, y2)
    c.setFillColor(MUTED)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - 8, y2 + 4)
    p.lineTo(x2 - 8, y2 - 4)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def table(c, rows, x, y, widths, size=13):
    for r, row in enumerate(rows):
        if r == 0:
            c.setFillColor(SOFT)
            c.rect(x, y - 8, sum(widths), 26, stroke=0, fill=1)
        c.setFont('Helvetica-Bold' if r == 0 else 'Helvetica', size)
        c.setFillColor(INK)
        cx = x
        for cell, w in zip(row, widths):
            c.drawString(cx + 8, y, cell)
            cx += w
        c.setStrokeColor(LINE)
        c.line(x, y - 9, x + sum(widths), y - 9)
        y -= 30
    return y


def main():
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle('AfyaPlus Health Ops - Module 4 capstone')

    header(c, 1, 'One door for clinic coordinators', 'Problem and user')
    bullets(c, ['Clinic coordinators juggle three separate tools from this module: triage, stock and listing checks',
                '  each with its own login, rules and logs',
                'User: AfyaPlus clinical_ops staff and partner clinics in western Kenya',
                'Decision supported: what happens next (send to clinic, reorder, review a listing)',
                'The system recommends; people decide. No diagnosis, no prescribing'])
    c.showPage()

    header(c, 2, 'Official AfyaPlus path, real artefacts', 'Path chosen and why')
    bullets(c, ['AfyaPlus Module 4 Capstone (not the domain alternative)',
                'Reuse, not rewrite: Week 5 knowledge, Week 6 API + JWT, Week 7 MCP tool + cache,',
                '  Week 8 pinned prompt (same sha 85e5cb1d...), Week 9 security, Week 10 catalog scorer',
                'Stub mode everywhere: deterministic tests, no API key, $0 this week',
                'Dataset: 300 synthetic intent rows + 10 SokoniHub listings in a separate folder'])
    c.showPage()

    header(c, 3, 'Architecture and module boundaries', 'services/triage is the only door')
    box(c, 40, 250, 150, 90, 'Client', 'POST /token\nPOST /triage')
    box(c, 230, 230, 230, 130, 'services/triage/app.py',
        'JWT 401\ninjection guard 400\nrouter (config.json)\nRBAC 403 + audit.jsonl')
    arrow(c, 190, 295, 228, 295)
    box(c, 520, 345, 400, 80, 'triage: stub model + Week 7 cache', 'pinned prompt 1.2.0 + RAG over Week 5 knowledge')
    box(c, 520, 250, 400, 80, 'logistics_lookup: MCP check_stock', 'one allowlisted clinic, role re-checked in the tool')
    box(c, 520, 155, 400, 80, 'catalog_mismatch: Week 10 lab-bow-v1', 'services/catalog with its own SokoniHub fixture')
    for y in (385, 290, 195):
        arrow(c, 460, 295, 518, y)
    box(c, 230, 70, 230, 100, 'audit.jsonl',
        'actor, role, action, outcome\npayload redacted then hashed\ntriage text: hash only', fill=white)
    arrow(c, 345, 230, 345, 172)
    c.setFont('Helvetica', 12)
    c.setFillColor(MUTED)
    c.drawString(48, 40, 'Data boundary: fixtures/ (clinical, synthetic) and services/catalog/fixtures/ (marketplace) never mix.')
    c.drawString(48, 22, 'tests/unit/test_fixture_separation.py fails the build if they do.')
    c.showPage()

    header(c, 4, 'Skill coverage: every skill has a file', 'skill_matrix.md + integration_map.json')
    table(c, [['Skill', 'Week', 'Where in the repo'],
              ['API or agent path', '6', 'services/triage/app.py, auth.py'],
              ['Cost / MCP tools', '7', 'agents/tools/logistics.py, model.py cache'],
              ['Pin / versioning', '8', 'services/triage/prompts/pin.json, corpus_pin.json'],
              ['Security hygiene', '9', 'tests/test_security_smoke.py, services/triage/security/'],
              ['RAG / grounded lookup', '5', 'services/rag/retriever.py + knowledge/'],
              ['Eval / test', '11', 'tests/unit, integration, perf; evals/golden.jsonl'],
              ['Optional multimodal', '10', 'services/catalog (own fixtures)']],
          48, H - 140, [260, 70, 530], size=14)
    c.setFont('Helvetica', 13)
    c.setFillColor(MUTED)
    c.drawString(48, 70, 'integration_map.json: 10 artefacts, every path checked on disk by check_integration_map.py')
    c.showPage()

    header(c, 5, 'Live demo: python run_demo.py', 'Backup: evidence/demo_transcript.txt')
    table(c, [['Request', 'Result'],
              ['GET /health', '200, prompt 1.2.0 sha 85e5cb1d..., model triage-stub-v1'],
              ['"My child has had a fever since yesterday"', 'medium, grounded in faq-fever'],
              ['"Chest pain and difficulty breathing"', 'high (red-flag floor), faq-danger-signs'],
              ['"How much ORS stock is at C04?"', 'MCP check_stock: 5 units, reorder needed'],
              ['"stock of ORS at *"', 'refused: one allowlisted clinic only (400)'],
              ['"Check the listing photo for NK-99"', 'Week 10 lane: flagged for review'],
              ['no token / partner triage / injection', '401 / 403 / 400']],
          48, H - 140, [420, 440], size=13)
    c.showPage()

    header(c, 6, 'Testing evidence', 'pytest pyramid + eval gate, all in CI')
    bullets(c, ['Unit (default): 45 passed - router, gold fixture, service functions, MCP tool, pins',
                'Security smoke: 9 passed - redaction, JWT 401, injection 400, RBAC 403, clean audit',
                'Integration -m integration: 4 passed + live httpx /health; perf -m perf: p95 0.025 s',
                'Golden-set eval: 30/32 = 0.94, gate 0.90; both misses fall back to triage',
                'Fixture incident: test went red on 28 rows, router fixed (not the test), green again'])
    c.showPage()

    header(c, 7, 'Security and compliance choices', 'Week 9 carried over')
    bullets(c, ['Authentication is not authorisation: JWT on /triage, then a role matrix (403)',
                'Refuse before spending: instruction-like text gets 400 before any tool or model',
                'No bulk export: check_stock answers for one allowlisted clinic; "*" refused',
                'Audit log redacted then hashed; health text kept as a hash only',
                'Pins on the prompt and the knowledge corpus; edits fail closed at start-up',
                'No secrets in git history (tested); clinical and marketplace fixtures never mixed'])
    c.showPage()

    header(c, 8, 'Cost table with assumptions', 'docs/cost_analysis.md')
    table(c, [['Call type', 'Calls', 'Total', 'Assumption'],
              ['Tests, eval, demo (stub)', '0 live', '$0', 'no key used this week'],
              ['Live demo, if wired', '~10', '~$0.0004', '$0.0000371 per call (Week 7 tokens)'],
              ['2,000 triage/day', '60k/mo', '~$2.23/mo', 'gpt-4o-mini list price'],
              ['+ Week 7 cache (0.60 hits)', '24k/mo', '~$0.89/mo', 'hit rate from Week 7 fixture']],
          48, H - 140, [300, 110, 130, 320], size=14)
    c.setFont('Helvetica', 14)
    c.setFillColor(MUTED)
    c.drawString(48, 150, 'Tokens are about 1% of the all-in cost (Week 7): people and hosting dominate.')
    c.showPage()

    header(c, 9, 'What works vs what is deferred', 'docs/build_checkpoint.md')
    c.setFont('Helvetica-Bold', 18)
    c.setFillColor(ACCENT)
    c.drawString(48, H - 140, 'Works now')
    c.drawString(500, H - 140, 'Deferred (said, not claimed)')
    bullets(c, ['One command, end to end, stub mode', 'Auth, RAG, MCP tool, catalog lane',
                'Pins, smoke, eval in CI', 'Measured perf, fixture checks'], x=48, y=H - 180, size=15, width=400)
    bullets(c, ['Live LLM (no key; stub only)', 'Cloud / Docker deploy (not executed live)',
                'LLM agent loop over MCP', 'Week 4 fine-tuned model', 'Classmate peer review (solo, declared)'],
            x=500, y=H - 180, size=15, width=420)
    c.showPage()

    header(c, 10, 'Process and next steps', 'git flow and review')
    bullets(c, ['Three feature branches -> PR #1 Monday, PR #2 Tuesday, PR #3 Thursday',
                'Each PR: template, CI green, checklist review comment, merge commit',
                'review_log.md: date, PR, reviewer (solo, declared), outcomes and follow-ups',
                'Next: a classifier router gated by the golden set',
                'Then: the live model behind a flag, with the stub kept for CI'])
    c.showPage()
    c.save()
    print('wrote', OUT.relative_to(ROOT).as_posix())


if __name__ == '__main__':
    main()
