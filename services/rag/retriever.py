"""Grounded lookup (Week 5 RAG idea, stub answerer): TF-IDF retrieval over a small, pinned
document set, and an answer that only quotes what it retrieved, with the source id.

Corpus:
  knowledge/clinic_faq.json        7 short teaching passages (not clinical guidance)
  knowledge/week5_knowledge.json   copied from afyaplus-multimodal-intake (Week 5): poster
                                   captions and field-report summaries; NOT HEALTH-RELATED
                                   items are dropped at load
Both files are sha256-pinned in knowledge/corpus_pin.json; a silent edit fails closed.
No embeddings and no model: deterministic, free, testable.
"""
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

KNOWLEDGE = Path(__file__).resolve().parent / 'knowledge'
STOP = {'the', 'a', 'an', 'and', 'or', 'of', 'to', 'in', 'is', 'are', 'my', 'has', 'have', 'with', 'for',
        'on', 'at', 'it', 'be', 'i', 'what', 'should', 'do', 'how', 'image', 'shows', 'assessment', 'clear'}


def tokens(text: str) -> list[str]:
    return [t for t in re.findall(r'[a-z]+', text.lower()) if t not in STOP and len(t) > 2]


def verify_corpus_pin() -> None:
    pin = json.loads((KNOWLEDGE / 'corpus_pin.json').read_text(encoding='utf-8'))
    for name, expected in pin.items():
        got = hashlib.sha256((KNOWLEDGE / name).read_bytes()).hexdigest()
        if got != expected:
            raise RuntimeError(f'CORPUS PIN MISMATCH {name}: {got[:12]} != {expected[:12]}')


def load_docs() -> list[dict]:
    verify_corpus_pin()
    docs = [{'id': d['id'], 'text': d['title'] + '. ' + d['text']}
            for d in json.loads((KNOWLEDGE / 'clinic_faq.json').read_text(encoding='utf-8'))]
    for d in json.loads((KNOWLEDGE / 'week5_knowledge.json').read_text(encoding='utf-8')):
        if 'NOT HEALTH-RELATED' in d['text']:
            continue
        body = re.sub(r'^Assessment: \w+\s*', '', d['text']).strip()
        docs.append({'id': 'wk5:' + d['source'], 'text': body})
    return docs


class Retriever:
    def __init__(self, docs: list[dict] | None = None):
        self.docs = docs if docs is not None else load_docs()
        self.tf = [Counter(tokens(d['text'])) for d in self.docs]
        df = Counter(t for tf in self.tf for t in tf)
        n = len(self.docs)
        self.idf = {t: math.log((1 + n) / (1 + c)) + 1 for t, c in df.items()}
        self.vecs = [self._weigh(tf) for tf in self.tf]

    def _weigh(self, tf: Counter) -> dict:
        v = {t: c * self.idf.get(t, 0.0) for t, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {t: x / norm for t, x in v.items()}

    def search(self, query: str, k: int = 2) -> list[tuple[float, dict]]:
        q = self._weigh(Counter(tokens(query)))
        scored = [(round(sum(q.get(t, 0.0) * w for t, w in v.items()), 4), d)
                  for v, d in zip(self.vecs, self.docs)]
        return [(s, d) for s, d in sorted(scored, key=lambda x: (-x[0], x[1]['id'])) if s > 0][:k]


def first_sentence(text: str) -> str:
    return re.split(r'(?<=[.!?])\s', text.strip(), maxsplit=1)[0]


def grounded_answer(question: str, retriever: Retriever, k: int = 2) -> dict:
    """Stub answerer: quote the best passage, cite every retrieved id, admit when nothing matched."""
    hits = retriever.search(question, k)
    if not hits:
        return {'answer': 'No clinic guidance in the knowledge base matches this; ask a clinician.',
                'sources': [], 'grounded': False}
    best = hits[0][1]
    return {'answer': first_sentence(best['text'].split('. ', 1)[-1]), 'sources': [d['id'] for _, d in hits],
            'grounded': True}
