import pytest


@pytest.mark.parametrize(
    "field,value",
    [
        ("raw_confidence", -0.1),
        ("raw_confidence", True),
        ("raw_confidence", 1.1),
        ("observed_state", "BLOCKED"),
        ("recorded_at", "2026-01-01T00:00:00"),
        ("recorded_at", "2999-01-01T00:00:00Z"),
        ("id", "bad-uuid"),
        ("source_id", "invalid/source"),
        ("notes", "x" * 1001),
        ("unexpected", True),
    ],
)
def test_invalid_input_never_persists(client, headers, payload, field, value):
    payload[field] = value
    response = client.post("/api/v1/observations", json=payload, headers=headers)
    assert response.status_code == 422
    assert len(client.get("/api/v1/observations?scenario_id=cyclone-demo").json()) == 6


@pytest.mark.parametrize("field", ["source_id", "scenario_id"])
def test_unknown_reference(client, headers, payload, field):
    payload[field] = "not-present"
    assert client.post("/api/v1/observations", json=payload, headers=headers).status_code == 404
