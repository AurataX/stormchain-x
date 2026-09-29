import asyncio
import os
from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.schema import CreateSchema

from app.core.database import connect

URL = os.getenv("TEST_DATABASE_URL", "")


@pytest.mark.skipif(not URL, reason="Set TEST_DATABASE_URL to a dedicated PostgreSQL database")
def test_generated_sql_executes_without_schema_drift():
    assert make_url(URL).database.endswith("_test")

    async def check():
        engine, _ = connect(URL)
        try:
            async with engine.connect() as connection:
                transaction = await connection.begin()
                try:
                    name = "schema_test_" + uuid4().hex
                    await connection.execute(CreateSchema(name))
                    await connection.execute(
                        text("SELECT set_config('search_path', :path, true)"),
                        {"path": f"{name},public"},
                    )
                    path = Path(__file__).resolve().parents[1] / "database/schema.sql"
                    for statement in path.read_text(encoding="utf-8").split(";"):
                        if statement.strip():
                            await connection.execute(text(statement))
                    assert await connection.scalar(text("SELECT count(*) FROM assets")) == 0
                finally:
                    await transaction.rollback()
        finally:
            await engine.dispose()

    asyncio.run(check())
