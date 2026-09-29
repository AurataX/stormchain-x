from datetime import datetime
from uuid import UUID

from app.schemas.common import Output


class RecoveryPlanOutput(Output):
    id: UUID
    scenario_id: str
    version: int
    total_cost_cents: int
    duration_minutes: int
    plan_payload: dict
    deterministic_rationale: dict
    generated_at: datetime
