def summarize_plan(record):
    snapshot = record.deterministic_rationale["inputs"]
    return {
        "scenario_id": record.scenario_id,
        "version": record.version,
        "generated_at": record.generated_at,
        "as_of": snapshot["parameters"]["as_of"],
        "cost_cents": record.total_cost_cents,
        "duration_minutes": record.duration_minutes,
        "actions": record.plan_payload["actions"],
        "solver": record.plan_payload["solver"],
        "verification_priority": record.plan_payload["verification_priority"][:10],
        "assumptions": record.plan_payload["assumptions"],
    }
