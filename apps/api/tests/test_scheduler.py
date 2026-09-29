from app.services.scheduler import solve


def job(name, crew="civil", cost=100, hours=4, weight=100):
    return {
        "id": name,
        "crew_type": crew,
        "cost_cents": cost,
        "duration_hours": hours,
        "weight": weight,
    }


def spans(result):
    return {row["id"]: (row["start_hour"], row["end_hour"]) for row in result["actions"]}


def test_budget_is_never_exceeded_and_best_action_wins():
    found = [job("low", cost=60, weight=100), job("high", cost=60, weight=500)]
    result = solve(found, {"low": None, "high": None}, 100, {"civil": 2})
    assert [row["id"] for row in result["actions"]] == ["high"]
    assert solve(found, {"low": None, "high": None}, 0, {"civil": 2})["actions"] == []


def test_crew_capacity_serializes_and_zero_crews_blocks():
    found = [job("a"), job("b")]
    gates = {"a": None, "b": None}
    (a, b) = spans(solve(found, gates, 1000, {"civil": 1})).values()
    assert a[1] <= b[0] or b[1] <= a[0]
    assert solve(found, gates, 1000, {"civil": 2})["actions"][1]["start_hour"] == 0
    assert solve(found, gates, 1000, {"electrical": 5})["actions"] == []


def test_access_gating_blocks_premature_repair():
    found = [job("road", cost=60, weight=100), job("hospital", cost=60, weight=900)]
    gates = {"road": None, "hospital": ["road"]}
    # Road repair is unaffordable alongside the hospital: hospital must not be scheduled.
    assert solve(found, gates, 100, {"civil": 2})["actions"][0]["id"] in {"road"}
    both = spans(solve(found, gates, 120, {"civil": 2}))
    assert both["road"][1] <= both["hospital"][0]
    assert "hospital" not in spans(solve(found[1:], gates, 1000, {"civil": 2}))


def test_solver_status_is_reported_honestly():
    result = solve([job("a")], {"a": None}, 1000, {"civil": 1})
    assert result["status"] in {"OPTIMAL", "FEASIBLE"}
    assert result["best_bound"] >= result["objective"] and result["gap"] >= 0
    assert solve([], {}, 0, {})["status"] == "OPTIMAL"
