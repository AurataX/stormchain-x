def blocked_assets(graph, intrinsic, assessments, rng):
    blocked = set()
    for node in sorted(graph):
        kind = graph.nodes[node]["type_id"]
        if kind == "road":
            closed = rng.random() < assessments[node]["passability"]["probabilities"]["BLOCKED"]
            if intrinsic[node] == 0 or closed:
                blocked.add(node)
        elif kind == "depot" and intrinsic[node] < 0.5:
            blocked.add(node)
    return blocked
