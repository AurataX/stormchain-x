from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import session
from app.models import Asset, Dependency
from app.schemas.asset import AssetDetail, DependencyOutput, FeatureCollection
from app.schemas.common import Identifier
from app.services.assets import detail, feature

router = APIRouter(prefix="/api/v1", tags=["Infrastructure"])
Database = Annotated[AsyncSession, Depends(session)]


@router.get("/assets", response_model=FeatureCollection)
async def assets(db: Database, limit: int = Query(100, ge=1, le=500), offset: int = Query(0, ge=0)):
    rows = await db.scalars(select(Asset).order_by(Asset.id).offset(offset).limit(limit))
    return {"features": [feature(row) for row in rows], "limit": limit, "offset": offset}


@router.get("/assets/{asset_id}", response_model=AssetDetail)
async def asset(asset_id: Identifier, scenario_id: Identifier, db: Database):
    return await detail(db, asset_id, scenario_id)


@router.get("/dependencies", response_model=list[DependencyOutput])
async def dependencies(
    db: Database, limit: int = Query(100, ge=1, le=500), offset: int = Query(0, ge=0)
):
    rows = await db.scalars(select(Dependency).order_by(Dependency.id).offset(offset).limit(limit))
    return rows.all()
