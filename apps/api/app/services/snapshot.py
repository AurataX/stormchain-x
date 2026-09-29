import platform

import networkx
from fastapi import HTTPException
from sqlalchemy import select

from app.models import Asset, AssetType, Dependency, Observation, ObservationSource, Scenario
from app.schemas.asset import AssetOutput, DependencyOutput
from app.schemas.observation import ObservationOutput
from app.schemas.scenario import ScenarioOutput, SourceOutput


async def capture(database, request):
    scenario = await database.get(Scenario, request.scenario_id)
    if scenario is None:
        raise HTTPException(404, "Scenario not found")
    snapshot = {
        "runtime": {"python": platform.python_version(), "networkx": networkx.__version__},
        "parameters": request.model_dump(mode="json"),
        "scenario": ScenarioOutput.model_validate(scenario).model_dump(),
    }
    groups = [
        ("assets", Asset, AssetOutput, 100),
        ("dependencies", Dependency, DependencyOutput, 500),
        ("sources", ObservationSource, SourceOutput, 100),
    ]
    for name, model, schema, maximum in groups:
        rows = (await database.scalars(select(model).order_by(model.id).limit(maximum + 1))).all()
        if len(rows) > maximum:
            raise HTTPException(422, f"Simulation supports at most {maximum} {name}")
        snapshot[name] = [schema.model_validate(row).model_dump(mode="json") for row in rows]
    reports = (
        await database.scalars(
            select(Observation)
            .where(
                Observation.scenario_id == request.scenario_id,
                Observation.recorded_at <= request.as_of,
                Observation.received_at <= request.as_of,
            )
            .order_by(Observation.id)
            .limit(10001)
        )
    ).all()
    if len(reports) > 10000:
        raise HTTPException(422, "Snapshot exceeds 10000 observations")
    snapshot["observations"] = [
        ObservationOutput.model_validate(row).model_dump(mode="json") for row in reports
    ]
    types = await database.scalars(select(AssetType).order_by(AssetType.id))
    snapshot["types"] = {
        row.id: {"category": row.category, "weight": row.criticality_weight} for row in types
    }
    return snapshot
