import asyncio
import json
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.core.config import Settings
from app.services import vertex_briefing


class FakeClient:
    def __init__(self, answer):
        self.answer = answer
        self.aio = self
        self.models = self

    async def generate_content(self, **kwargs):
        return SimpleNamespace(text=json.dumps(self.answer))

    async def aclose(self):
        pass

    def close(self):
        pass


def test_vertex_takes_precedence_and_validates_citations(monkeypatch):
    calls = []
    answer = {"answer": "Saved synthetic plan.", "citation_ids": ["plan-v1"]}

    def factory(**kwargs):
        calls.append(kwargs)
        return FakeClient(answer)

    monkeypatch.setattr(vertex_briefing.genai, "Client", factory)
    settings = Settings(
        gemini_api_key="test-key", vertex_project="test-project", vertex_location="global"
    )
    result = asyncio.run(vertex_briefing.generate(settings, "Explain", {"plan-v1": "saved"}))
    assert result.citation_ids == ["plan-v1"]
    assert calls == [{"vertexai": True, "project": "test-project", "location": "global"}]

    answer["citation_ids"] = ["invented-source"]
    with pytest.raises(HTTPException) as error:
        asyncio.run(vertex_briefing.generate(settings, "Explain", {"plan-v1": "saved"}))
    assert error.value.status_code == 502
