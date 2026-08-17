"""Unit tests for personalized prequential observer adaptations."""

from __future__ import annotations

from mammal.personalization.history import ParticipantPrequentialHistory
from mammal.personalization.models import PersonalizedPrequentialObserver


def test_personalized_observer_cold_start():
    obs = PersonalizedPrequentialObserver()
    inp = {
        "trial_id": "trl_cold_01",
        "domain": "world_geography",
        "human_locked_answer": "Paris",
        "options": ["Paris", "Lyon"],
        "prequential_history": None,
    }
    pred = obs.predict(inp)
    assert pred.observer_id == "personalized_prequential"
    assert pred.predicted_probability_correct == 0.75
    assert pred.confidence == 75.0


def test_personalized_observer_adapts_to_overconfidence_history():
    obs = PersonalizedPrequentialObserver()
    # History with high domain accuracy (90%) and overconfidence bias (+10%)
    history = ParticipantPrequentialHistory(
        participant_id="part_001",
        target_trial_id="trl_05",
        total_prior_trials=10,
        overall_accuracy=0.85,
        domain_accuracy={"world_geography": 0.90},
        mean_reported_confidence=95.0,
        calibration_bias=0.10,
        mean_latency_ms=600.0,
    )

    inp = {
        "trial_id": "trl_05",
        "domain": "world_geography",
        "human_locked_answer": "Paris",
        "options": ["Paris", "Lyon"],
        "human_response_latency_ms": 500.0,
        "prequential_history": history,
    }
    pred = obs.predict(inp)
    # Predicted probability blends base (0.75) and domain accuracy (0.90) -> ~0.825 + latency bonus
    assert pred.predicted_probability_correct > 0.80
    # Confidence reflects calibration bias adjustment
    assert pred.confidence > 90.0
