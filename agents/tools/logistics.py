"""The AfyaPlus logistics MCP tool (Week 7 server, Week 9 hardening), in stub mode.

check_stock(item, clinic_id) answers for ONE allowlisted clinic and returns the smallest
useful dictionary. "*" and unknown ids get a 400-shaped error before any lookup; an empty
allowlist is a 500 (config failure). The caller's role is re-checked here (RBAC inside the
tool, not only at the API).

Stub mode = the router calls check_stock() in-process, no LLM agent loop. The same function
is registered on a real FastMCP server, so `python -m agents.tools.logistics` serves it
over stdio and tests/unit/test_logistics_tool.py calls it through an MCP client session.
Data: data/clinics.json and data/clinics_allowlist.json, copied from afyaplus-week9.
"""
import json
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from services.triage.security.rbac import allowed

DATA = Path(__file__).resolve().parent / 'data'
ALLOWLIST_PATH = DATA / 'clinics_allowlist.json'
CLINICS = {c['id']: c for c in json.loads((DATA / 'clinics.json').read_text(encoding='utf-8'))['clinics']}
VALID_ITEMS = ['amoxicillin', 'ors_sachets', 'malaria_kits']
REORDER_THRESHOLD = 10

mcp = FastMCP('afyaplus-logistics')


def load_allowlist() -> set[str]:
    if not ALLOWLIST_PATH.exists():
        return set()
    return {str(x).strip().upper() for x in json.loads(ALLOWLIST_PATH.read_text(encoding='utf-8')).get('clinics', [])}


def check_stock_as(role: str, item: str, clinic_id: str) -> dict:
    if not allowed(role, 'check_stock'):
        return {'error': f"role '{role or 'none'}' may not call check_stock", 'code': 403}
    known = load_allowlist()
    if not known:
        return {'error': 'clinic allowlist is empty or missing', 'code': 500}
    cid = str(clinic_id or '').strip().upper()
    if cid not in known or cid not in CLINICS:
        return {'error': 'unknown clinic_id: ask about one allowlisted clinic (C01 to C05)', 'code': 400}
    key = str(item or '').strip().lower()
    if key not in VALID_ITEMS:
        return {'error': f'unknown item {item!r}', 'code': 400, 'valid_values': VALID_ITEMS}
    units = CLINICS[cid]['stock'][key]
    return {'clinic_id': cid, 'clinic': CLINICS[cid]['name'], 'item': key, 'units': units,
            'reorder_needed': units < REORDER_THRESHOLD}


@mcp.tool()
def check_stock(item: str, clinic_id: str) -> str:
    """Units of one item ("amoxicillin", "ors_sachets", "malaria_kits") at ONE clinic ("C01".."C05").
    Returns JSON {"clinic_id", "clinic", "item", "units", "reorder_needed"} or {"error", "code"}."""
    # The role is never a tool argument (a client could claim any role): the process that
    # starts the server sets CALLER_ROLE from the verified JWT, as in Week 9.
    return json.dumps(check_stock_as(os.getenv('CALLER_ROLE', ''), item, clinic_id))


if __name__ == '__main__':
    mcp.run()          # stdio transport
