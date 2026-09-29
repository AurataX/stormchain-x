import asyncio
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

from app.bootstrap import bootstrap
from app.core.config import Settings
from app.main import create_app

URL = os.getenv("TEST_DATABASE_URL", "")


@pytest.mark.skipif(not URL, reason="Set TEST_DATABASE_URL to a dedicated PostgreSQL database")
def test_postgres_ingestion_and_restart(payload):
    assert make_url(URL).database.endswith("_test")
    token = "postgres-integration-test-token"
    settings = Settings(URL, token)
    asyncio.run(bootstrap(settings))
    with TestClient(create_app(settings)) as client:
        assert client.get("/ready").json()["database"] == "postgresql"
        assert len(client.get("/api/v1/assets").json()["features"]) == 10
        response = client.post(
            "/api/v1/observations",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        assert response.json()["recorded_at"].endswith("Z")
    with TestClient(create_app(settings)) as restarted:
        rows = restarted.get(
            "/api/v1/observations?scenario_id=cyclone-demo&asset_id=road-main"
        ).json()
        assert any(row["id"] == payload["id"] for row in rows)
