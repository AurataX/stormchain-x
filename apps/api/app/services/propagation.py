from collections import defaultdict


def requirements(graph):
    incoming = defaultdict(lambda: defaultdict(list))
    for source, target, edge in graph.edges(data=True):
        kind = edge["dependency_type"]
        if kind == "ROAD_ACCESS":
            continue
        if kind == "TELECOM" and not edge["properties"].get("required_for_service", False):
            continue
        incoming[target][kind].append(source)
    return incoming


def propagate(graph, intrinsic, horizon, incoming=None):
    incoming = requirements(graph) if incoming is None else incoming
    levels = dict.fromkeys(graph, 0.0)
    for iteration in range(len(graph) + 2):
        updated = {}
        for node, asset in graph.nodes(data=True):
            supplies = []
            for kind, parents in incoming[node].items():
                supply = max(levels[parent] for parent in parents)
                if kind == "POWER":
                    reserves = asset["backup_systems"]
                    hours = max(
                        reserves.get("generator_hours", 0), reserves.get("battery_hours", 0)
                    )
                    supply = max(supply, min(1.0, hours / horizon))
                supplies.append(supply)
            updated[node] = min([intrinsic[node], *supplies])
        if updated == levels:
            return updated, iteration + 1
        levels = updated
    raise ValueError("Cascade failed to converge within the documented bound")
