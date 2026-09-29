from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import session
from app.core.security import require_operator
from app.models import Observation
from app.schemas.common import Identifier
from app.schemas.observation import ObservationInput, ObservationOutput
from app.services.observations import record

router = APIRouter(prefix="/api/v1/observations", tags=["Evidence"])
Database = Annotated[AsyncSession, Depends(session)]


@router.post(
    "", response_model=ObservationOutput, status_code=201, dependencies=[Depends(require_operator)]
)
async def create(payload: ObservationInput, db: Database):
    return await record(db, payload)


@router.get("", response_model=list[ObservationOutput])
async def observations(
    scenario_id: Identifier,
    db: Database,
    asset_id: Identifier | None = None,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    query = select(Observation).where(Observation.scenario_id == scenario_id)
    if asset_id:
        query = query.where(Observation.asset_id == asset_id)
    rows = await db.scalars(
        query.order_by(Observation.recorded_at.desc(), Observation.id).offset(offset).limit(limit)
    )
    return rows.all()
