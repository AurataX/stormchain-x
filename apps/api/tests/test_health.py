from fastapi.testclient import TestClient

from app.bootstrap import bootstrap
from app.core.config import Settings
from app.main import create_app


def test_uninitialized_database_is_not_ready(settings):
    with TestClient(create_app(settings)) as client:
        assert client.get("/health").status_code == 200
        assert client.get("/ready").status_code == 503
        response = client.get("/api/v1/assets")
        assert response.status_code == 503
        assert response.json() == {"detail": "Database unavailable"}


def test_unconfigured_writes_are_disabled(settings, payload):
    import asyncio

    asyncio.run(bootstrap(settings))
    with TestClient(create_app(Settings(settings.database_url, ""))) as client:
        assert client.post("/api/v1/observations", json=payload).status_code == 503


def test_openapi_and_scenario_contract(client):
    assert client.get("/openapi.json").status_code == 200
    scenario = client.get("/api/v1/scenarios/cyclone-demo").json()
    assert scenario["budget_cents"] == 250000000
    assert scenario["available_crews"]["civil"] == 2
    assert client.get("/api/v1/scenarios/missing").status_code == 404
    assert len(client.get("/api/v1/observation-sources").json()) == 2
