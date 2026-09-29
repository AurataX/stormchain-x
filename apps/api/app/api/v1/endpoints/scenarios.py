from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import session
from app.models import ObservationSource, Scenario
from app.schemas.common import Identifier
from app.schemas.scenario import ScenarioOutput, SourceOutput

router = APIRouter(prefix="/api/v1", tags=["Scenarios"])
Database = Annotated[AsyncSession, Depends(session)]


@router.get("/scenarios", response_model=list[ScenarioOutput])
async def scenarios(
    db: Database, limit: int = Query(100, ge=1, le=500), offset: int = Query(0, ge=0)
):
    rows = await db.scalars(select(Scenario).order_by(Scenario.id).offset(offset).limit(limit))
    return rows.all()


@router.get("/scenarios/{scenario_id}", response_model=ScenarioOutput)
async def scenario(scenario_id: Identifier, db: Database):
    row = await db.get(Scenario, scenario_id)
    if row is None:
        raise HTTPException(404, "Scenario not found")
    return row


@router.get("/observation-sources", response_model=list[SourceOutput])
async def sources(db: Database):
    rows = await db.scalars(select(ObservationSource).order_by(ObservationSource.id))
    return rows.all()
