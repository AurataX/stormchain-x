import asyncio
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.core.config import Settings
from app.services import briefing_lookup


class FakeClient:
    def __init__(self, ids):
        self.aio = self
        self.models = self
        self.ids = ids

    async def generate_content(self, **kwargs):
        call = SimpleNamespace(name="lookup_saved_facts", args={"ids": self.ids})
        return SimpleNamespace(function_calls=[call])

    async def aclose(self):
        pass

    def close(self):
        pass


def test_lookup_limits_model_to_saved_facts(monkeypatch):
    chosen = ["plan-v2"]
    monkeypatch.setattr(briefing_lookup, "_client", lambda settings: FakeClient(chosen))
    settings = Settings()
    sources = {"plan-v2": "saved", "asset-road-main": "saved asset"}
    selected = asyncio.run(briefing_lookup.select_sources(settings, "Why?", sources))
    assert selected == {"plan-v2": "saved"}
    chosen[:] = ["external-url"]
    with pytest.raises(HTTPException) as error:
        asyncio.run(briefing_lookup.select_sources(settings, "Why?", sources))
    assert error.value.status_code == 502
