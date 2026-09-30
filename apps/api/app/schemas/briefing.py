from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import Identifier


class BriefingInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    plan_id: UUID
    question: str = Field(default="Why did the plan change?", min_length=3, max_length=400)
    asset_id: Identifier | None = None


class BriefingOutput(BaseModel):
    answer: str
    citation_ids: list[str]
    sources: dict[str, str]
    plan_id: UUID
    plan_version: int
    model: str
    synthetic: bool = True
