from uuid import uuid4


def test_api_versions_increment_and_plans_are_retrievable(client, headers):
    body = {"scenario_id": "cyclone-demo", "as_of": "2026-09-28T13:00:00Z"}
    assert client.post("/api/v1/recovery/plans", json=body).status_code in {401, 403}
    first = client.post("/api/v1/recovery/plans", json=body, headers=headers)
    second = client.post("/api/v1/recovery/plans", json=body, headers=headers)
    assert (first.status_code, first.json()["version"], second.json()["version"]) == (201, 1, 2)
    plan = second.json()
    assert plan["deterministic_rationale"]["previous_version"] == 1
    assert plan["deterministic_rationale"]["diff"] == {
        "added": [],
        "removed": [],
        "rescheduled": [],
    }
    assert plan["plan_payload"]["actions"] == first.json()["plan_payload"]["actions"]
    assert plan["total_cost_cents"] <= 25_000_000
    scores = [row["score"] for row in plan["plan_payload"]["verification_priority"]]
    assert scores and scores == sorted(scores, reverse=True)
    listed = client.get("/api/v1/recovery/plans?scenario_id=cyclone-demo").json()
    assert [row["version"] for row in listed] == [2, 1]
    assert client.get("/api/v1/recovery/plans/" + plan["id"]).json() == plan
    assert client.get("/api/v1/recovery/plans/" + str(uuid4())).status_code == 404
    assert client.get("/api/v1/recovery/plans?scenario_id=nope").status_code == 404
    bad = client.post("/api/v1/recovery/plans", json={**body, "extra": 1}, headers=headers)
    assert bad.status_code == 422


def test_new_evidence_produces_next_version_with_diff(client, headers, payload):
    body = {"scenario_id": "cyclone-demo"}
    client.post("/api/v1/recovery/plans", json=body, headers=headers)
    payload.update(asset_id="road-main", access_status="BLOCKED")
    assert client.post("/api/v1/observations", json=payload, headers=headers).status_code == 201
    plan = client.post("/api/v1/recovery/plans", json=body, headers=headers).json()
    assert plan["version"] == 2
    assert "road-main" in {row["id"] for row in plan["plan_payload"]["actions"]}
