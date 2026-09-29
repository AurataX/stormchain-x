from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UTCDateTime, now


class Observation(Base):
    __tablename__ = "observations"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    scenario_id: Mapped[str] = mapped_column(ForeignKey("scenarios.id"))
    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"))
    source_id: Mapped[str] = mapped_column(ForeignKey("observation_sources.id"))
    observed_state: Mapped[str] = mapped_column(String(32))
    access_status: Mapped[str | None] = mapped_column(String(16))
    raw_confidence: Mapped[float]
    recorded_at: Mapped[datetime] = mapped_column(UTCDateTime())
    received_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=now)
    notes: Mapped[str] = mapped_column(String(1000), default="")
    __table_args__ = (
        CheckConstraint("raw_confidence BETWEEN 0 AND 1", name="confidence"),
        CheckConstraint("access_status IN ('OPEN','BLOCKED','UNKNOWN')", name="access"),
        CheckConstraint(
            "observed_state IN "
            "('OPERATIONAL','PARTIALLY_OPERATIONAL','DAMAGED','FAILED','UNKNOWN')",
            name="state",
        ),
        CheckConstraint("recorded_at <= received_at", name="time_order"),
        Index("ix_observations_scenario_asset_time", "scenario_id", "asset_id", "recorded_at"),
    )
