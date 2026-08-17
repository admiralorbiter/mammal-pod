"""Unit tests for baseline observers (uniform chance, base rate, solver, text heuristic)."""

from __future__ import annotations

from mammal.observers.baselines import (
    DeterministicSolverObserver,
    ItemBaseRateObserver,
    TextConfidenceHeuristicObserver,
    UniformChanceObserver,
)
from mammal.observers.runner import get_observer


def test_uniform_chance_observer():
    obs = UniformChanceObserver()
    inp = {
        "trial_id": "trl_001",
        "domain": "world_geography",
        "prompt_payload": {"question": "Capital of France?"},
        "options": ["A", "B", "C", "D"],
    }
    pred = obs.predict(inp)
    assert pred.observer_id == "uniform_chance"
    assert pred.predicted_probability_correct == 0.25
    assert pred.confidence == 25.0


def test_item_base_rate_observer():
    obs = ItemBaseRateObserver()
    inp = {
        "trial_id": "trl_002",
        "domain": "world_geography",
        "prompt_payload": {"question": "Capital of Germany?"},
        "options": ["Berlin", "Munich"],
    }
    pred = obs.predict(inp)
    assert pred.observer_id == "item_base_rate"
    assert pred.predicted_probability_correct == 0.78
    assert pred.confidence == 78.0


def test_deterministic_solver_observer():
    obs = DeterministicSolverObserver()
    inp = {
        "trial_id": "trl_003",
        "domain": "world_geography",
        "prompt_payload": {"question": "What is the capital city of France?"},
        "options": ["Lyon", "Paris", "Marseille"],
    }
    pred = obs.predict(inp)
    assert pred.observer_id == "deterministic_solver"
    assert pred.predicted_answer == "Paris"
    assert pred.predicted_probability_correct == 0.95


def test_text_confidence_heuristic_observer():
    obs = TextConfidenceHeuristicObserver()
    inp = {
        "trial_id": "trl_004",
        "domain": "world_geography",
        "prompt_payload": {"question": "What is the capital city of France?"},
        "options": ["Lyon", "Paris"],
        "human_locked_answer": "Paris",
    }
    pred = obs.predict(inp)
    assert pred.observer_id == "text_confidence_heuristic"
    assert pred.predicted_probability_correct == 0.82


def test_get_observer_factory():
    obs = get_observer("item_base_rate")
    assert obs.observer_id == "item_base_rate"
