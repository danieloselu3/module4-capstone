"""Which JWT role may use which routed tool (Week 9 matrix, adapted to the router's tools).

Authentication (a valid token) is not authorisation (a tool on this list). Unknown roles
get an empty set: deny by default.
"""
PARTNER = 'partner_clinic'
OPS = 'clinical_ops'

TOOLS_BY_ROLE = {
    PARTNER: {'logistics_lookup', 'check_stock'},
    OPS: {'triage', 'logistics_lookup', 'check_stock', 'catalog_mismatch'},
}


def allowed(role: str, tool: str) -> bool:
    return tool in TOOLS_BY_ROLE.get(role, set())
