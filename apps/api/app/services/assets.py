from fastapi import HTTPException
from sqlalchemy import or_, select

from app.models import Asset, Dependency, Observation, Scenario
from app.schemas.asset import AssetOutput


def feature(asset):
    properties = AssetOutput.model_validate(asset).model_dump(exclude={"geometry"})
    properties["assessment_status"] = "NOT_COMPUTED"
    return {"type": "Feature", "id": asset.id, "geometry": asset.geometry, "properties": properties}


async def detail(database, asset_id, scenario_id):
    asset = await database.get(Asset, asset_id)
    if asset is None or await database.get(Scenario, scenario_id) is None:
        raise HTTPException(404, "Asset or scenario not found")
    observations = await database.scalars(
        select(Observation)
        .where(Observation.asset_id == asset_id, Observation.scenario_id == scenario_id)
        .order_by(Observation.recorded_at.desc(), Observation.id)
        .limit(100)
    )
    edges = await database.scalars(
        select(Dependency)
        .where(or_(Dependency.source_asset_id == asset_id, Dependency.target_asset_id == asset_id))
        .order_by(Dependency.id)
    )
    return {"asset": asset, "observations": observations.all(), "dependencies": edges.all()}
