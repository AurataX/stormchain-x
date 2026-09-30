import json

from fastapi import HTTPException
from sqlalchemy import select

from app.models import RecoveryPlan
from app.services.briefing_plan_fact import summarize_plan


async def gather(database, request):
    plan = await database.get(RecoveryPlan, str(request.plan_id))
    if plan is None:
        raise HTTPException(404, "Recovery plan not found")
    query = select(RecoveryPlan).where(
        RecoveryPlan.scenario_id == plan.scenario_id,
        RecoveryPlan.version == plan.version - 1,
    )
    previous = await database.scalar(query) if plan.version > 1 else None
    snapshot = plan.deterministic_rationale["inputs"]
    assets = {row["id"]: row for row in snapshot["assets"]}
    if request.asset_id and request.asset_id not in assets:
        raise HTTPException(404, "Asset not found in saved plan")
    sources = {}

    def add(key, value):
        sources[key] = json.dumps(value, sort_keys=True, default=str)

    add(f"plan-v{plan.version}", summarize_plan(plan))
    if previous:
        add(f"plan-v{previous.version}", summarize_plan(previous))
        add("plan-diff", plan.deterministic_rationale["diff"])
    old_ids = (
        {row["id"] for row in previous.deterministic_rationale["inputs"]["observations"]}
        if previous
        else set()
    )
    reports = [
        row
        for row in snapshot["observations"]
        if row["id"] not in old_ids or row["asset_id"] == request.asset_id
    ]
    for row in reports[-20:]:
        add(
            f"observation-{row['id']}",
            {
                key: row[key]
                for key in (
                    "asset_id",
                    "source_id",
                    "observed_state",
                    "access_status",
                    "raw_confidence",
                    "recorded_at",
                    "received_at",
                )
            },
        )
    relevant = (
        {request.asset_id}
        if request.asset_id
        else {action["id"] for action in plan.plan_payload["actions"]}
    )
    for row in snapshot["dependencies"]:
        if row["source_asset_id"] in relevant or row["target_asset_id"] in relevant:
            add(f"dependency-{row['id']}", row)
    for asset_id in relevant:
        if asset_id in assets:
            add(
                f"asset-{asset_id}",
                {
                    "id": asset_id,
                    "name": assets[asset_id]["name"],
                    "type_id": assets[asset_id]["type_id"],
                },
            )
    return plan, sources
