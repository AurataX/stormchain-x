import json

from app.services.seed import FIXTURE


def snapshot():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return {
        "assets": data["assets"],
        "dependencies": data["dependencies"],
        "sources": data["observation_sources"],
        "observations": data["observations"],
        "types": {
            row["id"]: {"category": row["category"], "weight": row["criticality_weight"]}
            for row in data["asset_types"]
        },
        "parameters": {
            "as_of": "2026-09-28T13:00:00+00:00",
            "samples": 100,
            "seed": 42,
            "horizon_hours": 12,
            "scenario_id": "cyclone-demo",
        },
    }


def asset(identity, type_id="substation", backup=None):
    return {"id": identity, "type_id": type_id, "backup_systems": backup or {}}


def edge(source, target, kind="POWER", identity=None):
    return {
        "id": identity or source + target,
        "source_asset_id": source,
        "target_asset_id": target,
        "dependency_type": kind,
        "properties": {},
    }
