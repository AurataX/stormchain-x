from fastapi.testclient import TestClient

from app.main import create_app

REQUEST = {"scenario_id": "cyclone-demo", "as_of": "2026-09-28T13:00:00Z", "samples": 20}


def test_persisted_snapshot_and_restart(client, settings, headers, payload):
    response = client.post("/api/v1/simulation/cascade", json=REQUEST, headers=headers)
    assert response.status_code == 201
    run = response.json()
    assert len(run["inputs"]["observations"]) == 6
    assert client.post("/api/v1/observations", json=payload, headers=headers).status_code == 201
    repeated = client.post("/api/v1/simulation/cascade", json=REQUEST, headers=headers).json()
    assert repeated["fingerprint"] == run["fingerprint"]
    assert repeated["result"] == run["result"]
    with TestClient(create_app(settings)) as restarted:
        assert restarted.get("/api/v1/simulation/runs/" + run["id"]).json() == run


def test_snapshot_before_reports_arrived_is_unknown(client, headers):
    request = {**REQUEST, "as_of": "2026-09-28T12:59:00Z"}
    run = client.post("/api/v1/simulation/cascade", json=request, headers=headers).json()
    assert run["inputs"]["observations"] == []
    assert all("UNKNOWN" in row["flags"] for row in run["result"]["assessments"].values())


def test_graph_endpoint(client):
    response = client.get(
        "/api/v1/infrastructure/graph",
        params={"scenario_id": "cyclone-demo", "as_of": "2026-09-28T13:00:00Z"},
    )
    assert response.status_code == 200
    assert len(response.json()["dependencies"]) == 16
