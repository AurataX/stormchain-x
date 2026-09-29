from sqlalchemy import JSON, CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AssetType(Base):
    __tablename__ = "asset_types"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    category: Mapped[str] = mapped_column(String(32))
    criticality_weight: Mapped[float] = mapped_column(default=1.0)
    __table_args__ = (CheckConstraint("criticality_weight >= 0", name="weight"),)


class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    type_id: Mapped[str] = mapped_column(ForeignKey("asset_types.id"), index=True)
    geometry: Mapped[dict] = mapped_column(JSON)
    capacity_metrics: Mapped[dict] = mapped_column(JSON, default=dict)
    backup_systems: Mapped[dict] = mapped_column(JSON, default=dict)
    provenance: Mapped[str] = mapped_column(String(32), default="SYNTHETIC")
