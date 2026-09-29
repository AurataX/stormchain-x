def test_non_ascii_bearer_is_rejected(client, payload):
    response = client.post(
        "/api/v1/observations",
        json=payload,
        headers=[(b"Authorization", b"Bearer \xff")],
    )
    assert response.status_code == 401


def test_nonfinite_confidence_returns_validation_error(client, headers, payload):
    import json

    payload["raw_confidence"] = float("nan")
    response = client.post(
        "/api/v1/observations",
        content=json.dumps(payload),
        headers={**headers, "Content-Type": "application/json"},
    )
    assert response.status_code == 422
