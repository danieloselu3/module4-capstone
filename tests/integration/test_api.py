"""Integration layer (pytest -m integration): the whole HTTP flow through FastAPI's TestClient."""
import pytest
from fastapi.testclient import TestClient

from services.triage.app import app

pytestmark = pytest.mark.integration
client = TestClient(app)


def login(user='mercy', pw='logistics2026'):
    r = client.post('/token', json={'username': user, 'password': pw})
    assert r.status_code == 200
    return {'Authorization': f"Bearer {r.json()['access_token']}"}


def test_health_reports_pins():
    body = client.get('/health').json()
    assert body['status'] == 'ok' and body['mode'] == 'stub'
    assert body['prompt_version'] == '1.2.0' and body['prompt_sha256'].startswith('85e5cb1d')


def test_end_to_end_three_routes():
    h = login()
    tri = client.post('/triage', json={'text': 'My child has a fever since yesterday'}, headers=h).json()
    assert tri['route'] == 'triage' and tri['urgency'] == 'medium' and tri['sources']
    stock = client.post('/triage', json={'text': 'How much ORS stock is at C04?'}, headers=h).json()
    assert stock['result']['units'] == 5 and stock['result']['reorder_needed'] is True
    cat = client.post('/triage', json={'text': 'Check listing photo for NK-99'}, headers=h).json()
    assert cat['result']['flag'] is True


def test_wrong_password_is_401():
    assert client.post('/token', json={'username': 'mercy', 'password': 'wrongpass1'}).status_code == 401


def test_bad_body_is_422():
    assert client.post('/triage', json={'text': 'x' * 1001}, headers=login()).status_code == 422
