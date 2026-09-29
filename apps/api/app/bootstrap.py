import asyncio
from pathlib import Path

from sqlalchemy import text

from app.core.config import Settings
from app.core.database import connect
from app.core.migrations import migrate_observation_access
from app.models import Base
from app.services.seed import seed

SPATIAL = Path(__file__).resolve().parents[1] / "database" / "postgis.sql"


async def bootstrap(settings=None):
    engine, sessions = connect((settings or Settings()).database_url)
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
            await migrate_observation_access(connection)
            if engine.dialect.name == "postgresql":
                for statement in SPATIAL.read_text(encoding="utf-8").split(";"):
                    if statement.strip():
                        await connection.execute(text(statement))
        async with sessions() as database:
            await seed(database)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(bootstrap())
    print("Schema initialized; synthetic seed inserted without overwriting existing rows.")
