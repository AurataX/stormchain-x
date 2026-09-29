import hashlib
import json
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette.concurrency import run_in_threadpool

from app.models import RecoveryPlan
from app.services.plan_builder import PLANNER_VERSION, diff, plan
from app.services.snapshot import capture


async def latest(database, scenario_id):
    query = select(RecoveryPlan).where(RecoveryPlan.scenario_id == scenario_id)
    return await database.scalar(query.order_by(RecoveryPlan.version.desc()).limit(1))


async def create(database, request):
    inputs = await capture(database, request)
    payload = await run_in_threadpool(plan, inputs)
    previous = await latest(database, request.scenario_id)
    canonical = json.dumps({"planner": PLANNER_VERSION, "inputs": inputs}, sort_keys=True)
    record = RecoveryPlan(
        id=str(uuid4()),
        scenario_id=request.scenario_id,
        version=(previous.version if previous else 0) + 1,
        total_cost_cents=sum(row["cost_cents"] for row in payload["actions"]),
        duration_minutes=60 * max((row["end_hour"] for row in payload["actions"]), default=0),
        plan_payload=payload,
        deterministic_rationale={
            "planner_version": PLANNER_VERSION,
            "fingerprint": hashlib.sha256(canonical.encode()).hexdigest(),
            "previous_version": previous.version if previous else None,
            "diff": diff(previous.plan_payload if previous else None, payload),
            "inputs": inputs,
        },
    )
    database.add(record)
    try:
        await database.commit()
    except IntegrityError:
        await database.rollback()
        raise HTTPException(409, "Concurrent plan creation; retry") from None
    await database.refresh(record)
    return record


async def listing(database, scenario_id, limit):
    query = select(RecoveryPlan).where(RecoveryPlan.scenario_id == scenario_id)
    rows = await database.scalars(query.order_by(RecoveryPlan.version.desc()).limit(limit))
    return rows.all()
