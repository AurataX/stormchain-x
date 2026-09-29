from copy import deepcopy

import pytest

from app.services.fusion import assess
from tests.engine_helpers import snapshot


def test_missing_conflict_and_normalization():
    results = assess(snapshot())
    assert "UNKNOWN" in results["hospital-north"]["flags"]
    assert results["hospital-north"]["probabilities"]["FAILED"] == 0.25
    assert "CONFLICTING" in results["substation-east"]["flags"]
    assert all(sum(row["probabilities"].values()) == pytest.approx(1) for row in results.values())


def test_half_life_decay_and_staleness():
    inputs = snapshot()
    initial = assess(inputs)["road-main"]
    inputs["parameters"]["as_of"] = "2026-09-28T19:00:00+00:00"
    later = assess(inputs)["road-main"]
    assert later["evidence"][0]["weight"] == pytest.approx(initial["evidence"][0]["weight"] / 2)
    inputs["parameters"]["as_of"] = "2026-09-30T13:00:00+00:00"
    assert "STALE" in assess(inputs)["road-main"]["flags"]


def test_duplicate_polling_does_not_add_confidence():
    inputs = snapshot()
    original = assess(inputs)["road-main"]["probabilities"]
    duplicate = deepcopy(inputs["observations"][0])
    duplicate["id"] = "repeated-poll"
    inputs["observations"].append(duplicate)
    assert assess(inputs)["road-main"]["probabilities"] == original
    duplicate["observed_state"] = "UNKNOWN"
    assert "UNKNOWN" in assess(inputs)["road-main"]["flags"]
