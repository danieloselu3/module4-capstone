"""AfyaPlus Health Ops message API: one authenticated door, three routed tools, stub mode.

    uvicorn services.triage.app:app --port 8080

POST /token    -> JWT (Week 6)
POST /triage   -> JWT required (401), injection guard (400) BEFORE any tool, router picks a
                  tool from config.json, RBAC on the tool (403), audit row (Week 9):
                    triage            stub model + Week 7 cache + RAG grounding (Week 5) + pin (Week 8)
                    logistics_lookup  MCP check_stock in stub mode (Weeks 7 and 9)
                    catalog_mismatch  Week 10 SokoniHub scorer, its own fixtures
GET  /health   -> open; reports the pins
handle_message() is the plain-function core, so unit tests call it without HTTP.
"""
import re
import uuid

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from agents.router import CONFIG, route
from agents.tools.logistics import VALID_ITEMS, check_stock_as
from services.catalog.mismatch import score_sku
from services.rag.retriever import Retriever, grounded_answer
from services.triage import model
from services.triage.auth import auth_router, current_user
from services.triage.pins import load_pinned_prompt
from services.triage.security import audit_log
from services.triage.security.injection_guard import triage_or_reject
from services.triage.security.rbac import OPS, allowed

PIN, SYSTEM_PROMPT = load_pinned_prompt()        # fails closed on an edited prompt file
RETRIEVER = Retriever()                          # fails closed on an edited knowledge file
ITEM_WORDS = {'amoxicillin': 'amoxicillin', 'ors': 'ors_sachets', 'malaria': 'malaria_kits'}


def _clinic_id(text: str) -> str | None:
    m = re.search(r'\bC0?\d\b|\*', text, flags=re.I)
    return m.group(0).upper() if m else None


def _item(text: str) -> str | None:
    low = text.lower()
    return next((v for k, v in ITEM_WORDS.items() if k in low), None)


def handle_message(payload: dict, stub: bool = True, role: str = OPS) -> dict:
    """Route one message to one tool and return a JSON-able dict with status ok|needs_input|error."""
    if not stub:
        raise NotImplementedError('live model path is not wired in this capstone (README fallbacks)')
    text = str(payload.get('text') or '')
    tool = route(text)
    if not allowed(role, tool):
        return {'status': 'error', 'code': 403, 'route': tool, 'detail': f"role '{role}' may not use {tool}"}
    if tool == 'logistics_lookup':
        clinic, item = _clinic_id(text), _item(text)
        if not clinic or not item:
            return {'status': 'needs_input', 'route': tool,
                    'detail': f'Name one clinic (C01-C05) and one item ({", ".join(VALID_ITEMS)}).'}
        result = check_stock_as(role, item, clinic)
        status = 'error' if 'error' in result else 'ok'
        return {'status': status, 'route': tool, 'tool': 'mcp:check_stock (stub mode)', 'result': result}
    if tool == 'catalog_mismatch':
        m = re.search(r'\b[A-Z]{2,3}-\d{2}\b', text.upper())
        if not m:
            return {'status': 'needs_input', 'route': tool, 'detail': 'Name one SokoniHub SKU, e.g. NK-99.'}
        result = score_sku(m.group(0))
        return {'status': 'error' if 'error' in result else 'ok', 'route': tool, 'result': result}
    result, cache = model.cached_triage(text, PIN['sha256'], PIN['model_id'])
    rag = grounded_answer(text, RETRIEVER)
    return {'status': 'ok', 'route': 'triage', 'urgency': result['urgency'], 'advice': result['advice'],
            'guidance': rag['answer'], 'sources': rag['sources'], 'model_id': PIN['model_id'],
            'prompt_version': PIN['prompt_version'], 'cache': cache}


class Message(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    text: str = Field(min_length=2, max_length=1000)


app = FastAPI(title=CONFIG['project_name'], version='1.0.0')
app.include_router(auth_router)


@app.get('/health')
def health():
    return {'status': 'ok', 'service': CONFIG['project_name'], 'mode': 'stub',
            'model_id': PIN['model_id'], 'prompt_version': PIN['prompt_version'],
            'prompt_sha256': PIN['sha256'], 'knowledge_docs': len(RETRIEVER.docs)}


@app.post('/triage')
def triage(body: Message, request: Request, user: dict = Depends(current_user)):
    trace = request.headers.get('X-Request-ID') or uuid.uuid4().hex[:8]
    if not triage_or_reject(body.text).get('ok'):
        audit_log.record(actor=user['sub'], role=user['role'], action='message', resource='/triage',
                         outcome='rejected_400', trace_id=trace, payload=body.text)
        raise HTTPException(status_code=400, detail='Request refused: it looks like instructions to the system.')
    out = handle_message({'text': body.text}, stub=True, role=user['role'])
    audit_log.record(actor=user['sub'], role=user['role'], action=f"message:{out['route']}",
                     resource='/triage', outcome=str(out.get('code') or out['status']), trace_id=trace,
                     payload=body.text, keep_text=out['route'] != 'triage')   # health text: hash only
    if out.get('code') == 403:
        raise HTTPException(status_code=403, detail=out['detail'])
    return {**out, 'trace_id': trace, 'handled_for': user['sub']}
