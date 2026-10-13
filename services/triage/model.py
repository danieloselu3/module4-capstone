"""The triage model in stub mode (Week 6 keyword stub) behind a Week 7 response cache.

Stub mode is deterministic and free: urgency from red-flag words, advice from a template,
grounded with the top clinic-guidance passage from services/rag. A live gpt-4o-mini path
is deliberately not wired in this capstone (README fallbacks: no live OpenAI key).
"""
import hashlib

URGENT_WORDS = ['chest pain', 'bleeding', 'unconscious', 'cannot breathe', "can't breathe",
                'seizure', 'convulsion', 'not breathing', 'fainted']
MEDIUM_WORDS = ['fever', 'vomiting', 'diarrhoea', 'diarrhea', 'cough', 'rash', 'headache', 'pain']

_cache: dict[str, dict] = {}
metrics = {'hits': 0, 'misses': 0}


def stub_triage(message: str) -> dict:
    text = message.lower()
    if any(w in text for w in URGENT_WORDS):
        return {'urgency': 'high', 'advice': 'Warning signs reported: go to the nearest clinic now.'}
    if any(w in text for w in MEDIUM_WORDS):
        return {'urgency': 'medium', 'advice': 'See a clinician within 24 hours; return sooner if it gets worse.'}
    return {'urgency': 'low', 'advice': 'Rest, drink fluids and monitor; contact the clinic if it changes.'}


def cache_key(message: str, prompt_sha: str, model_id: str) -> str:
    """Week 7 exact-match key: the prompt sha is in it, so a new prompt never reuses old answers."""
    norm = ' '.join(message.lower().split())
    return hashlib.sha256(f'{model_id}|{prompt_sha[:12]}|{norm}'.encode()).hexdigest()


def cached_triage(message: str, prompt_sha: str, model_id: str) -> tuple[dict, str]:
    key = cache_key(message, prompt_sha, model_id)
    if key in _cache:
        metrics['hits'] += 1
        return _cache[key], 'HIT'
    metrics['misses'] += 1
    _cache[key] = stub_triage(message)
    return _cache[key], 'MISS'


def reset() -> None:
    _cache.clear()
    metrics.update(hits=0, misses=0)
