"""Unit layer for the real service functions in stub mode: triage + cache + RAG + pins, catalog."""
import hashlib
import json
from pathlib import Path

import pytest

from services.catalog.mismatch import score_sku
from services.rag.retriever import Retriever, grounded_answer
from services.triage import model
from services.triage.app import PIN, handle_message
from services.triage.pins import PROMPTS, load_pinned_prompt

RETRIEVER = Retriever()


@pytest.mark.parametrize('text,urgency', [
    ('chest pain and cannot breathe', 'high'),
    ('my child has a fever', 'medium'),
    ('general question about opening hours', 'low'),
])
def test_triage_urgency_and_safety_floor(text, urgency):
    out = handle_message({'text': text})
    assert out['route'] == 'triage' and out['urgency'] == urgency


def test_triage_is_grounded_in_retrieved_guidance():
    out = handle_message({'text': 'my child has a fever since yesterday'})
    assert out['sources'][0] == 'faq-fever' and 'malaria' in out['guidance']


@pytest.mark.parametrize('question,top', [
    ('diarrhoea at home, should I give ORS?', 'faq-ors'),
    ('chest pain and difficulty breathing', 'faq-danger-signs'),
    ('cough for three weeks with night sweats', 'faq-cough'),
    ('can you give me a medicine dose', 'faq-medicines'),
])
def test_rag_retrieval_on_fixed_questions(question, top):
    hits = RETRIEVER.search(question)
    assert hits and hits[0][1]['id'] == top


def test_rag_admits_when_nothing_matches():
    out = grounded_answer('how do I fix a car engine', RETRIEVER)
    assert out['grounded'] is False and out['sources'] == []


def test_week7_cache_hits_on_a_repeat():
    first = handle_message({'text': 'Fever two days'})
    again = handle_message({'text': '  fever   TWO days '})
    assert (first['cache'], again['cache']) == ('MISS', 'HIT')
    assert model.metrics == {'hits': 1, 'misses': 1}


def test_pin_sha_matches_the_prompt_file_and_week8():
    pin, text = load_pinned_prompt()
    assert hashlib.sha256((PROMPTS / pin['prompt_file']).read_bytes()).hexdigest() == pin['sha256']
    assert pin['sha256'].startswith('85e5cb1d7efb')             # afyaplus-week8 1.2.0, unchanged
    assert PIN['model_id'] == 'triage-stub-v1' and 'Never prescribe' in text


def test_live_path_is_not_pretended():
    with pytest.raises(NotImplementedError):
        handle_message({'text': 'hello'}, stub=False)


def test_catalog_lane_gold_pair():
    assert handle_message({'text': 'listing photo KND-01'})['result']['flag'] is False
    assert handle_message({'text': 'listing photo NK-99'})['result']['flag'] is True
    assert score_sku('XX-00')['code'] == 400


def test_corpus_pin_covers_both_knowledge_files():
    pin = json.loads(Path('services/rag/knowledge/corpus_pin.json').read_text(encoding='utf-8'))
    assert set(pin) == {'clinic_faq.json', 'week5_knowledge.json'}
