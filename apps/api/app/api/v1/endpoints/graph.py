from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import session
from app.schemas.assessment import GraphOutput
from app.schemas.simulation import SnapshotInput
from app.services.fusion import assess
from app.services.snapshot import capture
from app.services.topology import access_assessment, build_graph

router = APIRouter(prefix="/api/v1", tags=["Infrastructure"])


@router.get("/infrastructure/graph", response_model=GraphOutput)
async def graph(
    parameters: Annotated[SnapshotInput, Query()],
    database: Annotated[AsyncSession, Depends(session)],
):
    snapshot = await capture(database, parameters)
    assessments = assess(snapshot)
    return {
        "scenario_id": parameters.scenario_id,
        "as_of": snapshot["parameters"]["as_of"],
        "assets": snapshot["assets"],
        "dependencies": snapshot["dependencies"],
        "assessments": assessments,
        "access": access_assessment(build_graph(snapshot), assessments),
    }
