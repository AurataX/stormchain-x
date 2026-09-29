def test_seed_geojson_and_dependency_references(client):
    assert client.get("/health").status_code == 200
    assert client.get("/ready").json()["database"] == "sqlite"
    collection = client.get("/api/v1/assets").json()
    assert collection["type"] == "FeatureCollection"
    assert len(collection["features"]) == 10
    identities = {feature["id"] for feature in collection["features"]}
    for feature in collection["features"]:
        assert feature["geometry"]["type"] in {"Point", "LineString"}
        assert feature["properties"]["provenance"] == "SYNTHETIC"
        assert feature["properties"]["assessment_status"] == "NOT_COMPUTED"
    edges = client.get("/api/v1/dependencies").json()
    assert len(edges) == 16
    assert all(edge["source_asset_id"] in identities for edge in edges)
    assert all(edge["target_asset_id"] in identities for edge in edges)


def test_detail_preserves_missing_and_conflicting_evidence(client):
    endpoint = "/api/v1/assets/{}?scenario_id=cyclone-demo"
    unknown = client.get(endpoint.format("hospital-north")).json()
    assert unknown["observations"] == []
    conflict = client.get(endpoint.format("substation-east")).json()
    assert {row["observed_state"] for row in conflict["observations"]} == {
        "FAILED",
        "PARTIALLY_OPERATIONAL",
    }
    assert client.get(endpoint.format("missing")).status_code == 404
    assert client.get("/api/v1/assets?limit=0").status_code == 422
    assert client.get("/api/v1/assets?limit=501").status_code == 422
