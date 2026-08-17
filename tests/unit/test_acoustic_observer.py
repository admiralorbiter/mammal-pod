"""Unit tests for acoustic prosody observer predictions."""

from __future__ import annotations

from mammal.observers.acoustic_observer import AcousticProsodyObserver


def test_acoustic_prosody_observer_confident_speech():
    obs = AcousticProsodyObserver()
    inp = {
        "trial_id": "trl_conf_001",
        "human_locked_answer": "Paris",
        "human_response_latency_ms": 600.0,
        "acoustic_features": {
            "rising_terminal_pitch": False,
            "pitch_jitter_pct": 1.5,
            "shimmer_pct": 2.0,
        },
    }
    pred = obs.predict(inp)
    assert pred.observer_id == "acoustic_prosody"
    assert pred.confidence >= 80.0
    assert pred.predicted_probability_correct >= 0.80


def test_acoustic_prosody_observer_hesitant_uptalk_speech():
    obs = AcousticProsodyObserver()
    inp = {
        "trial_id": "trl_hesitant_002",
        "human_locked_answer": "Paris",
        "human_response_latency_ms": 2500.0,
        "acoustic_features": {
            "rising_terminal_pitch": True,  # Uptalk question tone
            "pitch_jitter_pct": 9.5,  # High vocal tremor
            "shimmer_pct": 10.0,
        },
    }
    pred = obs.predict(inp)
    assert pred.confidence < 30.0
    assert pred.predicted_probability_correct < 0.30
