"""Change for your project: nothing. Point SERVICE_URL at your own endpoint if renamed."""
import os
import httpx
import pytest

pytestmark = pytest.mark.integration


@pytest.mark.skipif(os.getenv("SERVICE_UP") != "1", reason="set SERVICE_UP=1 when the service is running")
def test_health_returns_200():
    r = httpx.get("http://localhost:8080/health", timeout=5)
    assert r.status_code == 200
