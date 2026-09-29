import asyncio
import os

import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url

from app.bootstrap import bootstrap
from app.core.config import Settings
from app.core.database import connect

URL = os.getenv("TEST_DATABASE_URL", "")


@pytest.mark.skipif(not URL, reason="Set TEST_DATABASE_URL to a dedicated PostgreSQL database")
def test_postgis_geometry_and_seed():
    assert make_url(URL).database.endswith("_test"), "Use a disposable *_test database"

    async def check():
        await bootstrap(Settings(URL, ""))
        await bootstrap(Settings(URL, ""))
        engine, sessions = connect(URL)
        try:
            async with sessions() as database:
                rows = (
                    await database.execute(
                        text(
                            "SELECT ST_SRID(geom), ST_IsValid(geom), "
                            "ST_GeometryType(geom) FROM assets"
                        )
                    )
                ).all()
                assert len(rows) == 10
                assert all(srid == 4326 and valid for srid, valid, _ in rows)
                assert {kind for _, _, kind in rows} == {"ST_Point", "ST_LineString"}
                indexes = await database.scalar(
                    text("SELECT count(*) FROM pg_indexes WHERE indexname = 'ix_assets_geom'")
                )
                assert indexes == 1
        finally:
            await engine.dispose()

    asyncio.run(check())
