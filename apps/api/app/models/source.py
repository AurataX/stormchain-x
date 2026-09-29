from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ObservationSource(Base):
    __tablename__ = "observation_sources"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    base_reliability: Mapped[float]
    half_life_seconds: Mapped[int]
    __table_args__ = (
        CheckConstraint("base_reliability > 0 AND base_reliability <= 1", name="reliability"),
        CheckConstraint("half_life_seconds > 0", name="half_life"),
    )
