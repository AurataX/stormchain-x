from typing import Literal

from pydantic import BaseModel

from app.schemas.common import Output
from app.schemas.observation import ObservationOutput


class AssetOutput(Output):
    id: str
    name: str
    type_id: str
    geometry: dict
    capacity_metrics: dict
    backup_systems: dict
    provenance: str


class DependencyOutput(Output):
    id: str
    source_asset_id: str
    target_asset_id: str
    dependency_type: str
    properties: dict


class Feature(BaseModel):
    type: Literal["Feature"] = "Feature"
    id: str
    geometry: dict
    properties: dict


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[Feature]
    limit: int
    offset: int


class AssetDetail(BaseModel):
    asset: AssetOutput
    observations: list[ObservationOutput]
    dependencies: list[DependencyOutput]
    history_limit: int = 100
