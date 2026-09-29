from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import session
from app.core.security import require_operator
from app.models import SimulationRun
from app.schemas.simulation import SimulationInput, SimulationOutput
from app.services.simulation import run

router = APIRouter(prefix="/api/v1/simulation", tags=["Simulation"])
Database = Annotated[AsyncSession, Depends(session)]


@router.post(
    "/cascade",
    response_model=SimulationOutput,
    status_code=201,
    dependencies=[Depends(require_operator)],
)
async def cascade(payload: SimulationInput, db: Database):
    return await run(db, payload)


@router.get("/runs/{run_id}", response_model=SimulationOutput)
async def retrieve(run_id: UUID, db: Database):
    record = await db.get(SimulationRun, str(run_id))
    if record is None:
        raise HTTPException(404, "Simulation run not found")
    return record
