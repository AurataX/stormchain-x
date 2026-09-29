from datetime import datetime

from app.services.distribution import distribution
from app.services.evidence import STATES, latest_reports, weighted


def assess(snapshot):
    as_of = datetime.fromisoformat(snapshot["parameters"]["as_of"])
    sources = {item["id"]: item for item in snapshot["sources"]}
    reports = latest_reports(snapshot["observations"])
    access_reports = latest_reports(
        [row for row in snapshot["observations"] if row.get("access_status") is not None]
    )
    result = {}
    for asset in snapshot["assets"]:
        evidence = [
            weighted(row, sources[row["source_id"]], as_of)
            for row in reports
            if row["asset_id"] == asset["id"]
        ]
        access_evidence = [
            weighted(row, sources[row["source_id"]], as_of)
            for row in access_reports
            if row["asset_id"] == asset["id"]
        ]
        result[asset["id"]] = {
            **distribution(evidence, "state", STATES),
            "evidence": evidence,
            "passability": {
                **distribution(access_evidence, "access_status", ("OPEN", "BLOCKED")),
                "evidence": access_evidence,
            },
        }
    return result
