from collections import defaultdict
from random import Random
from statistics import fmean, pvariance

from app.services.access_sampling import blocked_assets
from app.services.evidence import LEVELS, STATES
from app.services.propagation import propagate, requirements
from app.services.topology import reachable


def simulate(snapshot, graph, assessments):
    parameters = snapshot["parameters"]
    rng = Random(parameters["seed"])
    losses, iterations = [], []
    totals, access = defaultdict(float), defaultdict(int)
    incoming = requirements(graph)
    critical = {
        node: snapshot["types"][asset["type_id"]]["weight"]
        for node, asset in graph.nodes(data=True)
        if snapshot["types"][asset["type_id"]]["category"] in {"HEALTHCARE", "SHELTER"}
    }
    for _ in range(parameters["samples"]):
        intrinsic = {}
        for node in sorted(graph):
            weights = [assessments[node]["probabilities"][state] for state in STATES]
            intrinsic[node] = rng.choices(LEVELS, weights=weights)[0]
        blocked = blocked_assets(graph, intrinsic, assessments, rng)
        reached = reachable(graph, blocked)
        levels, count = propagate(graph, intrinsic, parameters["horizon_hours"], incoming)
        iterations.append(count)
        losses.append(sum(weight * (1 - levels[node]) for node, weight in critical.items()))
        for node in graph:
            totals[node] += levels[node]
            access[node] += node in reached
    samples = parameters["samples"]
    return {
        "expected_loss": fmean(losses),
        "loss_variance": pvariance(losses),
        "loss_unit": "weighted_critical_service_deficit",
        "max_loss": sum(critical.values()),
        "max_iterations": max(iterations),
        "mean_service": {n: totals[n] / samples for n in graph},
        "access_probability": {n: access[n] / samples for n in graph},
    }
