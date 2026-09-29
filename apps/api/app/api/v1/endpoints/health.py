from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError

from app.models import Asset, Observation, Scenario, SimulationRun

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    return {"status": "ok", "phase": 2}


@router.get("/ready")
async def ready(request: Request):
    try:
        async with request.app.state.sessions() as database:
            for model in (Asset, Observation, Scenario, SimulationRun):
                await database.execute(select(model).limit(1))
            if database.bind.dialect.name == "postgresql":
                await database.execute(text("SELECT PostGIS_Version(), geom FROM assets LIMIT 1"))
    except SQLAlchemyError:
        return JSONResponse({"status": "unavailable"}, status_code=503)
    return {"status": "ready", "database": request.app.state.engine.dialect.name}
