import pytest


@pytest.mark.parametrize(
    "field,value",
    [
        ("samples", 0),
        ("samples", 1001),
        ("seed", -1),
        ("horizon_hours", 0),
        ("as_of", "2999-01-01T00:00:00Z"),
        ("as_of", "2026-01-01T00:00:00"),
    ],
)
def test_simulation_input_bounds(client, headers, field, value):
    payload = {"scenario_id": "cyclone-demo", field: value}
    assert (
        client.post("/api/v1/simulation/cascade", json=payload, headers=headers).status_code == 422
    )


def test_simulation_auth_and_missing_scenario(client, headers):
    endpoint = "/api/v1/simulation/cascade"
    assert client.post(endpoint, json={"scenario_id": "cyclone-demo"}).status_code == 401
    assert (
        client.post(endpoint, json={"scenario_id": "missing"}, headers=headers).status_code == 404
    )


def test_graph_rejects_future_evaluation(client):
    response = client.get(
        "/api/v1/infrastructure/graph",
        params={"scenario_id": "cyclone-demo", "as_of": "2999-01-01T00:00:00Z"},
    )
    assert response.status_code == 422
