"""Change for your project: nothing. Update config.json route_keywords instead."""
from agents.router import route


def test_route_logistics():
    assert route("track delivery") == "logistics_lookup"


def test_route_default():
    assert route("general question") == "triage"


def test_service_runs_in_stub_mode():
    from services.triage.app import handle_message
    out = handle_message({"text": "hello"}, stub=True)
    assert out["status"] == "ok"

def test_pin_has_model_and_version():
    import json
    pin = json.loads(open("services/triage/prompts/pin.json").read())
    assert pin.get("model_id") and pin.get("prompt_version")