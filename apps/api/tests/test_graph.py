from app.services.topology import access_assessment, build_graph, reachable
from tests.engine_helpers import asset, edge


def test_directed_parallel_edges_and_alternative_routes():
    graph = build_graph(
        {
            "assets": [asset("d", "depot"), asset("r", "road"), asset("h")],
            "dependencies": [
                edge("d", "r", "ROAD_ACCESS"),
                edge("r", "h", "ROAD_ACCESS"),
                edge("r", "h", "POWER", "power"),
            ],
        }
    )
    assert graph.number_of_edges("r", "h") == 2
    assert reachable(graph, set()) == {"d", "r", "h"}
    assert reachable(graph, {"r"}) == {"d"}
    graph.add_edge("d", "h", dependency_type="ROAD_ACCESS")
    assert "h" in reachable(graph, {"r"})
    assert "d" not in reachable(graph, {"d"})


def test_unknown_road_is_not_reported_as_confirmed_failure():
    graph = build_graph(
        {
            "assets": [asset("d", "depot"), asset("r", "road"), asset("h")],
            "dependencies": [edge("d", "r", "ROAD_ACCESS"), edge("r", "h", "ROAD_ACCESS")],
        }
    )
    result = access_assessment(graph, {"r": {"flags": ["UNKNOWN"]}})
    assert result["h"] == "UNKNOWN"
    blocked = {"passability": {"flags": [], "probabilities": {"OPEN": 0.1, "BLOCKED": 0.9}}}
    assert access_assessment(graph, {"r": blocked})["h"] == "BLOCKED"
