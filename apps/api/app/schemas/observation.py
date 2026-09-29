from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator

from app.schemas.common import Identifier, Output


class AssetState(StrEnum):
    OPERATIONAL = "OPERATIONAL"
    PARTIALLY_OPERATIONAL = "PARTIALLY_OPERATIONAL"
    DAMAGED = "DAMAGED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class ObservationInput(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    id: UUID
    scenario_id: Identifier
    asset_id: Identifier
    source_id: Identifier
    observed_state: AssetState
    access_status: Literal["OPEN", "BLOCKED", "UNKNOWN"] | None = None
    raw_confidence: float = Field(ge=0, le=1, strict=True)
    recorded_at: AwareDatetime
    notes: str = Field(default="", max_length=1000)

    @field_validator("recorded_at")
    @classmethod
    def past_time(cls, value):
        if value > datetime.now(UTC):
            raise ValueError("Observation time cannot be in the future")
        return value.astimezone(UTC)


class ObservationOutput(Output):
    id: str
    scenario_id: str
    asset_id: str
    source_id: str
    observed_state: AssetState
    access_status: str | None
    raw_confidence: float
    recorded_at: datetime
    received_at: datetime
    notes: str
