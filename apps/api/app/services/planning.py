def _likely(report, states):
    return max(states, key=report["probabilities"].get)


def candidates(snapshot, assessments, catalog):
    """Repair candidates from fused evidence; missing evidence never implies damage."""
    found = []
    for asset in snapshot["assets"]:
        report = assessments[asset["id"]]
        if asset["type_id"] == "road":
            broken = _likely(report["passability"], ("OPEN", "BLOCKED")) == "BLOCKED"
        else:
            broken = (
                "UNKNOWN" not in report["flags"]
                and _likely(report, ("OPERATIONAL", "PARTIALLY_OPERATIONAL", "DAMAGED", "FAILED"))
                != "OPERATIONAL"
            )
        if broken and asset["type_id"] in catalog:
            action = catalog[asset["type_id"]]
            weight = snapshot["types"][asset["type_id"]]["weight"]
            found.append({"id": asset["id"], "weight": round(weight * 100), **action})
    return found


def prerequisites(graph, found):
    """None = ungated (no road predecessor, or one that needs no repair)."""
    ids = {item["id"] for item in found}
    result = {}
    for item in found:
        roads = [
            source
            for source, _, edge in graph.in_edges(item["id"], data=True)
            if edge["dependency_type"] == "ROAD_ACCESS"
        ]
        open_route = not roads or any(source not in ids for source in roads)
        result[item["id"]] = None if open_route else sorted(set(roads))
    return result


def verification_priority(assessments, assets, types, selected):
    """Heuristic criticality x entropy for uncertain unselected assets; not formal VoI."""
    ranked = []
    for asset in assets:
        report = assessments[asset["id"]]
        if asset["type_id"] == "road":
            report = report["passability"]
        if asset["id"] in selected or not report["flags"]:
            continue
        score = types[asset["type_id"]]["weight"] * report["entropy"]
        ranked.append({"asset_id": asset["id"], "score": score, "flags": report["flags"]})
    return sorted(ranked, key=lambda row: (-row["score"], row["asset_id"]))
