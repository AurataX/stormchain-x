import asyncio

from sqlalchemy import text

from app.core.database import connect
from app.core.migrations import migrate_observation_access


def test_access_migration_preserves_existing_evidence(settings):
    async def check():
        engine, _ = connect(settings.database_url)
        try:
            async with engine.begin() as connection:
                await connection.execute(text("CREATE TABLE observations (id TEXT PRIMARY KEY)"))
                await connection.execute(
                    text("INSERT INTO observations (id) VALUES ('old-report')")
                )
                await migrate_observation_access(connection)
                await migrate_observation_access(connection)
                rows = (
                    await connection.execute(text("SELECT id, access_status FROM observations"))
                ).all()
                assert rows == [("old-report", None)]
        finally:
            await engine.dispose()

    asyncio.run(check())
