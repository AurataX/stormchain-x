import hashlib
import json
from uuid import uuid4

from starlette.concurrency import run_in_threadpool

from app.models import SimulationRun
from app.services.cascade import simulate
from app.services.fusion import assess
from app.services.snapshot import capture
from app.services.topology import access_assessment, build_graph

ENGINE_VERSION = "cascade-0.2.0"


def evaluate(snapshot):
    assessments = assess(snapshot)
    graph = build_graph(snapshot)
    return {
        "assessments": assessments,
        "access": access_assessment(graph, assessments),
        "metrics": simulate(snapshot, graph, assessments),
        "assumptions": [
            "Synthetic evidence; uncalibrated weighted-count heuristic",
            "Independent asset sampling; no common hazard correlations",
            "Reserve hours are remaining at evaluation; no refueling",
            "Horizon-average service approximation; no repair scheduling",
        ],
    }


async def run(database, request):
    inputs = await capture(database, request)
    canonical = json.dumps(
        {"engine": ENGINE_VERSION, "inputs": inputs},
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    result = await run_in_threadpool(evaluate, inputs)
    record = SimulationRun(
        id=str(uuid4()),
        scenario_id=request.scenario_id,
        fingerprint=hashlib.sha256(canonical.encode()).hexdigest(),
        engine_version=ENGINE_VERSION,
        inputs=inputs,
        result=result,
    )
    database.add(record)
    await database.commit()
    await database.refresh(record)
    return record
