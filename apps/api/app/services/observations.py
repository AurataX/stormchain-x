from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models import Asset, Observation, ObservationSource, Scenario


async def record(database, payload):
    references = (
        (Asset, payload.asset_id),
        (Scenario, payload.scenario_id),
        (ObservationSource, payload.source_id),
    )
    for model, identity in references:
        resource = await database.get(model, identity)
        if resource is None:
            raise HTTPException(404, f"{model.__name__} not found")
        if model is Asset and payload.access_status is not None and resource.type_id != "road":
            raise HTTPException(422, "Access status is only supported for road assets")
    values = payload.model_dump()
    values["id"] = str(payload.id)
    observation = Observation(**values)
    database.add(observation)
    try:
        await database.commit()
    except IntegrityError:
        await database.rollback()
        raise HTTPException(409, "Observation conflicts with existing data") from None
    await database.refresh(observation)
    return observation
