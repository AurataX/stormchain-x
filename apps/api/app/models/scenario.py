from sqlalchemy import JSON, CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Scenario(Base):
    __tablename__ = "scenarios"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(1000))
    cyclone_category: Mapped[int]
    communication_mode: Mapped[str] = mapped_column(String(32))
    budget_cents: Mapped[int]
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    available_crews: Mapped[dict] = mapped_column(JSON)
    __table_args__ = (
        CheckConstraint("budget_cents >= 0", name="budget"),
        CheckConstraint("cyclone_category BETWEEN 1 AND 5", name="category"),
        CheckConstraint(
            "communication_mode IN ('NORMAL','DEGRADED','SEVERELY_DEGRADED','OFFLINE')",
            name="communication",
        ),
    )
