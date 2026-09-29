from app.services.actions import CATALOG
from app.services.fusion import assess
from app.services.planning import candidates, prerequisites, verification_priority
from app.services.scheduler import solve
from app.services.topology import build_graph

PLANNER_VERSION = "recovery-0.3.0"


def plan(snapshot):
    assessments = assess(snapshot)
    found = candidates(snapshot, assessments, CATALOG)
    scenario = snapshot["scenario"]
    result = solve(
        found,
        prerequisites(build_graph(snapshot), found),
        scenario["budget_cents"],
        scenario["available_crews"],
    )
    chosen = {row["id"] for row in result["actions"]}
    return {
        "solver": {key: value for key, value in result.items() if key != "actions"},
        "actions": result["actions"],
        "unselected": sorted(item["id"] for item in found if item["id"] not in chosen),
        "verification_priority": verification_priority(
            assessments, snapshot["assets"], snapshot["types"], chosen
        ),
        "assumptions": [
            "SYNTHETIC repair catalog; integer hours and cents",
            "Missing evidence is never treated as damage or closure",
            "Road already open or repaired earlier gates each action; no partial repairs",
            "Priority is criticality x entropy, a heuristic and not formal VoI",
        ],
    }


def diff(old, new):
    before = {row["id"]: row for row in old["actions"]} if old else {}
    after = {row["id"]: row for row in new["actions"]}
    return {
        "added": sorted(after.keys() - before.keys()),
        "removed": sorted(before.keys() - after.keys()),
        "rescheduled": sorted(
            key
            for key in before.keys() & after.keys()
            if before[key]["start_hour"] != after[key]["start_hour"]
        ),
    }
