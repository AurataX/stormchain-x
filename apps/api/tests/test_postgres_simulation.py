import asyncio
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

from app.bootstrap import bootstrap
from app.core.config import Settings
from app.main import create_app
from app.services.simulation import evaluate

URL = os.getenv("TEST_DATABASE_URL", "")


@pytest.mark.skipif(not URL, reason="Set TEST_DATABASE_URL to a dedicated PostgreSQL database")
def test_postgres_simulation_snapshot_replay():
    assert make_url(URL).database.endswith("_test")
    token = "postgres-simulation-test-token"
    settings = Settings(URL, token)
    asyncio.run(bootstrap(settings))
    with TestClient(create_app(settings)) as client:
        response = client.post(
            "/api/v1/simulation/cascade",
            json={"scenario_id": "cyclone-demo", "samples": 10, "as_of": "2026-09-28T13:00:00Z"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        record = response.json()
    with TestClient(create_app(settings)) as restarted:
        saved = restarted.get("/api/v1/simulation/runs/" + record["id"]).json()
        assert saved == record
        assert evaluate(saved["inputs"]) == saved["result"]
