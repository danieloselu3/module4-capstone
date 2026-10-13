"""Week 10 catalog lane (copied from sokonihub-mm/mismatch.py): lab-bow-v1 photo-tag vs
title cosine, threshold 0.25. Its SokoniHub fixture lives ONLY in services/catalog/fixtures/
and never mixes with the clinical fixtures in fixtures/ (tests/unit/test_fixture_separation.py).
"""
import json
import re
from pathlib import Path

CATALOG_PATH = Path(__file__).resolve().parent / 'fixtures' / 'sokonihub_catalog.json'
ENCODER_ID = 'lab-bow-v1'
VOCAB = ['kiondo', 'bag', 'sisal', 'navy', 'nike', 'shoe', 'white', 'leso', 'maize', 'cloth', 'red', 'woven',
         'kikoi', 'striped', 'flour', 'canvas', 'sandals', 'tyre', 'kanga', 'yellow']
THRESHOLD = 0.25


def tokens(text: str):
    return re.findall(r'[a-z0-9]+', text.lower())


def bow(toks):
    idx = {t: i for i, t in enumerate(VOCAB)}
    v = [0.0] * len(VOCAB)
    for t in toks:
        if t in idx:
            v[idx[t]] += 1.0
    return v


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    return dot / ((na * nb) or 1.0)


def load_catalog() -> dict:
    return {r['sku']: r for r in json.loads(CATALOG_PATH.read_text(encoding='utf-8'))}


def score_sku(sku: str) -> dict:
    row = load_catalog().get(sku.upper())
    if row is None:
        return {'error': f'unknown sku {sku!r}', 'code': 400}
    s = cosine(bow(row.get('image_tags') or []), bow(tokens(row.get('title') or '')))
    return {'sku': row['sku'], 'score': round(s, 4), 'flag': s < THRESHOLD, 'encoder': ENCODER_ID,
            'review': 'queued_for_human_review' if s < THRESHOLD else 'none'}
