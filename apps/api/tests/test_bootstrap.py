import asyncio

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.bootstrap import bootstrap
from app.core.database import connect
from app.models import Asset, Observation


def test_idempotent_seed_preserves_reports(client, settings, headers, payload):
    assert client.post("/api/v1/observations", json=payload, headers=headers).status_code == 201
    asyncio.run(bootstrap(settings))
    asyncio.run(bootstrap(settings))
    assert len(client.get("/api/v1/assets").json()["features"]) == 10
    assert len(client.get("/api/v1/observations?scenario_id=cyclone-demo").json()) == 7


def test_foreign_keys_reject_orphans(settings):
    async def check():
        await bootstrap(settings)
        engine, sessions = connect(settings.database_url)
        try:
            async with sessions() as database:
                database.add(Asset(id="orphan", name="Orphan", type_id="missing", geometry={}))
                try:
                    await database.commit()
                except IntegrityError:
                    await database.rollback()
                else:
                    raise AssertionError("Foreign key violation accepted")
                count = await database.scalar(select(func.count()).select_from(Observation))
                assert count == 6
        finally:
            await engine.dispose()

    asyncio.run(check())
