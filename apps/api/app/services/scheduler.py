from collections import defaultdict

from ortools.sat.python import cp_model

from app.services.gating import add_gates


def solve(found, gates, budget_cents, crews, seconds=10):
    """CP-SAT: end is 0 unless selected, so only chosen actions pay completion time."""
    horizon = max(1, sum(item["duration_hours"] for item in found))
    model = cp_model.CpModel()
    pick, start, end, spans = {}, {}, {}, defaultdict(list)
    for item in found:
        name, duration = item["id"], item["duration_hours"]
        pick[name] = model.NewBoolVar("pick_" + name)
        start[name] = model.NewIntVar(0, horizon, "start_" + name)
        end[name] = model.NewIntVar(0, horizon + duration, "end_" + name)
        model.Add(end[name] == start[name] + duration).OnlyEnforceIf(pick[name])
        model.Add(end[name] == 0).OnlyEnforceIf(pick[name].Not())
        model.Add(start[name] == 0).OnlyEnforceIf(pick[name].Not())
        spans[item["crew_type"]].append(
            model.NewOptionalFixedSizeIntervalVar(start[name], duration, pick[name], name)
        )
    add_gates(model, found, gates, pick, start, end)
    model.Add(sum(i["cost_cents"] * pick[i["id"]] for i in found) <= budget_cents)
    for crew, intervals in spans.items():
        model.AddCumulative(intervals, [1] * len(intervals), crews.get(crew, 0))
    big = len(found) * (horizon + 20) + 1
    model.Maximize(sum(i["weight"] * big * pick[i["id"]] for i in found) - sum(end.values()))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_workers = 1  # single worker keeps runs reproducible
    solver.parameters.random_seed = 0
    status = solver.StatusName(solver.Solve(model))
    solved = status in ("OPTIMAL", "FEASIBLE")
    actions = [
        {
            **item,
            "start_hour": solver.Value(start[item["id"]]),
            "end_hour": solver.Value(end[item["id"]]),
        }
        for item in found
        if solved and solver.Value(pick[item["id"]])
    ]
    actions.sort(key=lambda row: (row["start_hour"], row["id"]))
    objective = solver.ObjectiveValue() if solved else None
    bound = solver.BestObjectiveBound() if solved else None
    return {
        "status": status,
        "objective": objective,
        "best_bound": bound,
        "gap": None if not solved else abs(bound - objective) / max(1.0, abs(objective)),
        "actions": actions,
    }
