import asyncio
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.bootstrap import bootstrap
from app.core.config import Settings
from app.main import create_app

TOKEN = "local-test-token-with-at-least-24-characters"


@pytest.fixture
def settings(tmp_path):
    return Settings(f"sqlite+aiosqlite:///{tmp_path / 'test.db'}", TOKEN)


@pytest.fixture
def client(settings):
    asyncio.run(bootstrap(settings))
    with TestClient(create_app(settings)) as instance:
        yield instance


@pytest.fixture
def headers():
    return {"Authorization": f"Bearer {TOKEN}"}


@pytest.fixture
def payload():
    return {
        "id": str(uuid4()),
        "scenario_id": "cyclone-demo",
        "asset_id": "road-main",
        "source_id": "field",
        "observed_state": "FAILED",
        "raw_confidence": 0.95,
        "recorded_at": (datetime.now(UTC) - timedelta(minutes=1)).isoformat(),
        "notes": "SIMULATED road closure",
    }
