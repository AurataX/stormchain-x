from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import session
from app.core.security import require_operator
from app.models import RecoveryPlan, Scenario
from app.schemas.common import Identifier
from app.schemas.recovery import RecoveryPlanOutput
from app.schemas.simulation import SnapshotInput
from app.services.recovery import create, listing

router = APIRouter(prefix="/api/v1/recovery", tags=["Recovery"])
Database = Annotated[AsyncSession, Depends(session)]


@router.post(
    "/plans",
    response_model=RecoveryPlanOutput,
    status_code=201,
    dependencies=[Depends(require_operator)],
)
async def generate(payload: SnapshotInput, db: Database):
    return await create(db, payload)


@router.get("/plans", response_model=list[RecoveryPlanOutput])
async def plans(scenario_id: Identifier, db: Database, limit: int = Query(20, ge=1, le=100)):
    if await db.get(Scenario, scenario_id) is None:
        raise HTTPException(404, "Scenario not found")
    return await listing(db, scenario_id, limit)


@router.get("/plans/{plan_id}", response_model=RecoveryPlanOutput)
async def retrieve(plan_id: UUID, db: Database):
    record = await db.get(RecoveryPlan, str(plan_id))
    if record is None:
        raise HTTPException(404, "Recovery plan not found")
    return record
