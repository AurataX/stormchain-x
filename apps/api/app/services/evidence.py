from datetime import datetime

STATES = ("OPERATIONAL", "PARTIALLY_OPERATIONAL", "DAMAGED", "FAILED")
LEVELS = (1.0, 0.5, 0.25, 0.0)


def latest_reports(reports):
    latest = {}
    for report in reports:
        key = (report["asset_id"], report["source_id"])
        rank = (report["recorded_at"], report["received_at"], report["id"])
        previous = latest.get(key)
        if previous is None or rank > previous[0]:
            latest[key] = (rank, report)
    return [item[1] for item in sorted(latest.values(), key=lambda item: item[1]["id"])]


def weighted(report, source, as_of):
    age = max(0, (as_of - datetime.fromisoformat(report["recorded_at"])).total_seconds())
    half_life = source["half_life_seconds"]
    weight = source["base_reliability"] * report["raw_confidence"] * 2 ** (-age / half_life)
    return {
        "id": report["id"],
        "state": report["observed_state"],
        "access_status": report.get("access_status"),
        "weight": weight,
        "age_seconds": age,
        "stale": age > 2 * half_life,
    }
