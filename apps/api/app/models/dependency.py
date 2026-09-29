from sqlalchemy import JSON, CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Dependency(Base):
    __tablename__ = "dependencies"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source_asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    target_asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    dependency_type: Mapped[str] = mapped_column(String(32))
    properties: Mapped[dict] = mapped_column(JSON, default=dict)
    __table_args__ = (
        UniqueConstraint("source_asset_id", "target_asset_id", "dependency_type"),
        CheckConstraint("source_asset_id <> target_asset_id", name="no_self_edge"),
        CheckConstraint(
            "dependency_type IN ('POWER','WATER','TELECOM','ROAD_ACCESS')", name="type"
        ),
    )
