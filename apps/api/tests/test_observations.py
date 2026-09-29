from fastapi.testclient import TestClient

from app.main import create_app


def test_ingestion_duplicate_and_restart(client, settings, headers, payload):
    response = client.post("/api/v1/observations", json=payload, headers=headers)
    assert response.status_code == 201
    row = response.json()
    assert row["id"] == payload["id"]
    assert row["received_at"].endswith("Z")
    assert client.post("/api/v1/observations", json=payload, headers=headers).status_code == 409
    with TestClient(create_app(settings)) as restarted:
        rows = restarted.get("/api/v1/observations?scenario_id=cyclone-demo").json()
        assert sum(item["id"] == payload["id"] for item in rows) == 1


def test_auth_and_unknown_references(client, headers, payload):
    endpoint = "/api/v1/observations"
    assert client.post(endpoint, json=payload).status_code == 401
    assert (
        client.post(endpoint, json=payload, headers={"Authorization": "Bearer wrong"}).status_code
        == 401
    )
    payload["asset_id"] = "missing"
    assert client.post(endpoint, json=payload, headers=headers).status_code == 404
    assert len(client.get(endpoint + "?scenario_id=cyclone-demo").json()) == 6


def test_scenario_isolation_and_order(client):
    assert client.get("/api/v1/observations?scenario_id=other").json() == []
    rows = client.get("/api/v1/observations?scenario_id=cyclone-demo&limit=2").json()
    assert len(rows) == 2
    assert rows[0]["recorded_at"] >= rows[1]["recorded_at"]
