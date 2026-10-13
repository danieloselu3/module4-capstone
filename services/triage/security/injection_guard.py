"""Refuse instruction-like user text before any model, retriever or tool call (Week 9)."""
MAX_CHARS = 2000

OVERRIDE_PHRASES = (
    'ignore previous instructions',
    'ignore all instructions',
    'ignore all previous instructions',
    'disregard previous instructions',
    'you are now',
    'reveal the system prompt',
    'reveal your system prompt',
    'print your system prompt',
    'print your secret',
    'developer mode',
)


def looks_like_override(message: str) -> bool:
    m = ' '.join(message.strip().lower().split())
    return any(p in m for p in OVERRIDE_PHRASES)


def triage_or_reject(message: str) -> dict:
    if len(message) > MAX_CHARS:
        return {'error': 'rejected: payload too large', 'code': 400}
    if looks_like_override(message):
        return {'error': 'rejected: instruction-like input', 'code': 400}
    return {'ok': True, 'message': message}
