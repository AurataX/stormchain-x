from app.services.propagation import propagate
from app.services.topology import build_graph
from tests.engine_helpers import asset, edge


def test_power_water_cascade_and_backup_expiry():
    graph = build_graph(
        {
            "assets": [asset("p"), asset("w"), asset("h", "hospital", {"generator_hours": 12})],
            "dependencies": [edge("p", "w"), edge("p", "h"), edge("w", "h", "WATER")],
        }
    )
    levels, _ = propagate(graph, {"p": 0, "w": 1, "h": 1}, 12)
    assert levels["h"] == 0
    graph.remove_edge("w", "h", "wh")
    assert propagate(graph, {"p": 0, "w": 1, "h": 1}, 12)[0]["h"] == 1
    assert propagate(graph, {"p": 0, "w": 1, "h": 1}, 24)[0]["h"] == 0.5


def test_cycles_do_not_create_supply_and_redundancy_restores_it():
    graph = build_graph(
        {
            "assets": [asset("a"), asset("b"), asset("root")],
            "dependencies": [edge("a", "b"), edge("b", "a")],
        }
    )
    levels, count = propagate(graph, dict.fromkeys(graph, 1), 12)
    assert levels["a"] == levels["b"] == 0
    assert count <= len(graph) + 2
    graph.add_edge("root", "a", dependency_type="POWER", properties={})
    assert propagate(graph, dict.fromkeys(graph, 1), 12)[0]["b"] == 1
