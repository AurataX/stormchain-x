import asyncio

from app.core.database import connect
from app.models import Observation, Scenario


def test_other_scenario_evidence_is_excluded(client, settings, headers, payload):
    async def insert_other():
        engine, sessions = connect(settings.database_url)
        try:
            async with sessions() as database:
                original = await database.get(Scenario, "cyclone-demo")
                database.add(
                    Scenario(
                        id="other",
                        name="Other",
                        description="Test",
                        cyclone_category=4,
                        communication_mode="OFFLINE",
                        budget_cents=original.budget_cents,
                        available_crews={},
                    )
                )
                await database.commit()
                existing = await database.get(Observation, "00000000-0000-4000-8000-000000000001")
                database.add(
                    Observation(
                        id=payload["id"],
                        scenario_id="other",
                        asset_id="road-main",
                        source_id="field",
                        observed_state="FAILED",
                        raw_confidence=1,
                        recorded_at=existing.recorded_at,
                        received_at=existing.received_at,
                    )
                )
                await database.commit()
        finally:
            await engine.dispose()

    asyncio.run(insert_other())
    request = {"scenario_id": "cyclone-demo", "as_of": "2026-09-28T13:00:00Z", "samples": 1}
    run = client.post("/api/v1/simulation/cascade", json=request, headers=headers).json()
    assert len(run["inputs"]["observations"]) == 6
    assert all(row["scenario_id"] == "cyclone-demo" for row in run["inputs"]["observations"])
