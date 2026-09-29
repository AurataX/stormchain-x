from app.services.simulation import evaluate
from tests.engine_helpers import snapshot


def test_seeded_results_are_reproducible_and_bounded():
    inputs = snapshot()
    first = evaluate(inputs)
    assert evaluate(inputs) == first
    metrics = first["metrics"]
    assert 0 <= metrics["expected_loss"] <= metrics["max_loss"]
    assert metrics["loss_variance"] >= 0
    assert all(0 <= value <= 1 for value in metrics["mean_service"].values())
    assert all(0 <= value <= 1 for value in metrics["access_probability"].values())
    assert metrics["max_iterations"] <= len(inputs["assets"]) + 2
    inputs["parameters"]["seed"] = 43
    assert evaluate(inputs)["metrics"] != metrics


def test_single_sample_variance_is_zero():
    inputs = snapshot()
    inputs["parameters"]["samples"] = 1
    assert evaluate(inputs)["metrics"]["loss_variance"] == 0
