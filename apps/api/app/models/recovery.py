from datetime import datetime

from sqlalchemy import JSON, CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UTCDateTime, now


class RecoveryPlan(Base):
    __tablename__ = "recovery_plans"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    scenario_id: Mapped[str] = mapped_column(ForeignKey("scenarios.id"))
    version: Mapped[int]
    total_cost_cents: Mapped[int]
    duration_minutes: Mapped[int]
    plan_payload: Mapped[dict] = mapped_column(JSON)
    deterministic_rationale: Mapped[dict] = mapped_column(JSON)
    generated_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=now)
    __table_args__ = (
        UniqueConstraint("scenario_id", "version"),
        CheckConstraint("total_cost_cents >= 0", name="cost"),
        CheckConstraint("duration_minutes >= 0", name="duration"),
        CheckConstraint("version > 0", name="version"),
    )
