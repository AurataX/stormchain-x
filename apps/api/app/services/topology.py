import networkx as nx


def build_graph(snapshot):
    graph = nx.MultiDiGraph()
    for asset in snapshot["assets"]:
        graph.add_node(asset["id"], **asset)
    for edge in snapshot["dependencies"]:
        graph.add_edge(edge["source_asset_id"], edge["target_asset_id"], key=edge["id"], **edge)
    return graph


def reachable(graph, blocked):
    roads = nx.DiGraph()
    roads.add_nodes_from(node for node in graph if node not in blocked)
    roads.add_edges_from(
        (source, target)
        for source, target, edge in graph.edges(data=True)
        if edge["dependency_type"] == "ROAD_ACCESS"
        and source not in blocked
        and target not in blocked
    )
    reached = set()
    for node, asset in graph.nodes(data=True):
        if asset["type_id"] == "depot" and node not in blocked:
            reached.add(node)
            reached.update(nx.descendants(roads, node))
    return reached


def access_assessment(graph, assessments):
    blocked, uncertain = set(), set()
    for node, asset in graph.nodes(data=True):
        if asset["type_id"] not in {"road", "depot"}:
            continue
        report = assessments.get(node, {"flags": ["UNKNOWN"]})
        if asset["type_id"] == "road":
            if not report.get("flags", ["UNKNOWN"]) and report["probabilities"]["FAILED"] >= 0.75:
                blocked.add(node)
                continue
            report = report.get("passability", {"flags": ["UNKNOWN"]})
        if report["flags"]:
            uncertain.add(node)
        elif (
            report["probabilities"].get("BLOCKED", 0)
            + report["probabilities"].get("DAMAGED", 0)
            + report["probabilities"].get("FAILED", 0)
        ) >= 0.5:
            blocked.add(node)
    definite = reachable(graph, blocked | uncertain)
    possible = reachable(graph, blocked)
    return {
        node: "REACHABLE" if node in definite else "UNKNOWN" if node in possible else "BLOCKED"
        for node in graph
    }
