"""One MCP tool in stub mode: check_stock in-process and over a real MCP client session."""
import asyncio
import json

import pytest
from mcp.shared.memory import create_connected_server_and_client_session

from agents.tools import logistics
from services.triage.app import handle_message


def test_routed_stock_question_returns_the_minimal_row():
    out = handle_message({'text': 'stock of ors at C02'})
    assert out['route'] == 'logistics_lookup' and out['status'] == 'ok'
    assert out['result'] == {'clinic_id': 'C02', 'clinic': 'Vihiga Health Post', 'item': 'ors_sachets',
                             'units': 90, 'reorder_needed': False}


@pytest.mark.parametrize('clinic', ['*', 'all', 'C99', ''])
def test_wildcards_and_unknown_clinics_are_400(clinic):
    assert logistics.check_stock_as('clinical_ops', 'ors_sachets', clinic)['code'] == 400


def test_empty_allowlist_fails_closed_500(tmp_path, monkeypatch):
    empty = tmp_path / 'allow.json'
    empty.write_text('{"clinics": []}')
    monkeypatch.setattr(logistics, 'ALLOWLIST_PATH', empty)
    assert logistics.check_stock_as('clinical_ops', 'ors_sachets', 'C01')['code'] == 500


def test_unknown_role_is_denied_inside_the_tool():
    assert logistics.check_stock_as('admin', 'ors_sachets', 'C01')['code'] == 403


def _call(args: dict) -> dict:
    async def go():
        async with create_connected_server_and_client_session(logistics.mcp._mcp_server) as s:
            tools = {t.name for t in (await s.list_tools()).tools}
            assert tools == {'check_stock'}
            return json.loads((await s.call_tool('check_stock', args)).content[0].text)
    return asyncio.run(go())


def test_over_the_mcp_protocol_role_comes_from_the_server_env(monkeypatch):
    monkeypatch.setenv('CALLER_ROLE', 'partner_clinic')
    assert _call({'item': 'amoxicillin', 'clinic_id': 'C04'})['units'] == 0
    monkeypatch.delenv('CALLER_ROLE')
    assert _call({'item': 'amoxicillin', 'clinic_id': 'C04'})['code'] == 403      # no role, no data
