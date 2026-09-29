import json
from datetime import datetime
from pathlib import Path

from app.models import Asset, AssetType, Dependency, Observation, ObservationSource, Scenario

FIXTURE = Path(__file__).resolve().parents[2] / "data" / "coastal-district.json"
TABLES = (
    ("asset_types", AssetType),
    ("assets", Asset),
    ("observation_sources", ObservationSource),
    ("scenarios", Scenario),
    ("dependencies", Dependency),
    ("observations", Observation),
)


async def seed(database):
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    async with database.begin():
        for key, model in TABLES:
            for values in fixture[key]:
                if await database.get(model, values["id"]) is not None:
                    continue
                if model is Observation:
                    for field in ("recorded_at", "received_at"):
                        values[field] = datetime.fromisoformat(values[field])
                database.add(model(**values))
            await database.flush()
