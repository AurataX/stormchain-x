from datetime import UTC, datetime
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator

from app.schemas.common import Identifier, Output


class SnapshotInput(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    scenario_id: Identifier
    as_of: AwareDatetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("as_of")
    @classmethod
    def past_time(cls, value):
        if value > datetime.now(UTC):
            raise ValueError("Evaluation time cannot be in the future")
        return value.astimezone(UTC)


class SimulationInput(SnapshotInput):
    seed: int = Field(default=42, ge=0, le=2147483647, strict=True)
    samples: int = Field(default=200, ge=1, le=1000, strict=True)
    horizon_hours: float = Field(default=12, gt=0, le=168, strict=True)


class SimulationOutput(Output):
    id: UUID
    scenario_id: str
    fingerprint: str
    engine_version: str
    inputs: dict
    result: dict
    created_at: datetime
