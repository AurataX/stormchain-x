from copy import deepcopy
from random import Random

from app.services.access_sampling import blocked_assets
from app.services.fusion import assess
from app.services.topology import build_graph
from tests.engine_helpers import asset, snapshot


def test_damaged_road_can_be_open_and_operational_road_closed():
    graph = build_graph({"assets": [asset("road", "road")], "dependencies": []})
    assessments = {"road": {"passability": {"probabilities": {"BLOCKED": 0}}}}
    assert blocked_assets(graph, {"road": 0.25}, assessments, Random(1)) == set()
    assessments["road"]["passability"]["probabilities"]["BLOCKED"] = 1
    assert blocked_assets(graph, {"road": 1}, assessments, Random(1)) == {"road"}


def test_non_access_report_preserves_latest_explicit_access():
    inputs = snapshot()
    report = deepcopy(inputs["observations"][0])
    report.update(id="new-report", recorded_at="2026-09-28T12:45:00+00:00", access_status=None)
    original = assess(inputs)["road-main"]["passability"]
    inputs["observations"].append(report)
    assert assess(inputs)["road-main"]["passability"] == original


def test_access_input_is_road_only(client, headers, payload):
    payload["access_status"] = "BLOCKED"
    assert client.post("/api/v1/observations", json=payload, headers=headers).status_code == 201
    payload["asset_id"] = "hospital-central"
    assert client.post("/api/v1/observations", json=payload, headers=headers).status_code == 422
