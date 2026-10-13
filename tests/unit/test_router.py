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


# Tuesday Lab 2 "extend it yourself": two more gold cases
def test_gold_delivery_intent():
    assert route("Is the ORS delivery to C02 delayed?") == "logistics_lookup"


def test_gold_listing_photo_intent():
    assert route("The listing photo for NK-99 shows a bag") == "catalog_mismatch"
