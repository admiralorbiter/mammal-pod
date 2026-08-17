"""Unit tests for Personalization Gain computation and Rule 5 epistemic reporting."""

from __future__ import annotations

from mammal.analysis.personalization_gain import compute_personalization_gain


def test_personalization_gain_positive_improvement():
    # True outcomes: 8 correct, 2 incorrect
    outcomes = [True] * 8 + [False] * 2
    # Generic observer has flat confidence (70% on all)
    gen_confs = [70.0] * 10
    # Personalized observer predicts 92% on correct, 20% on incorrect (calibrated)
    pers_confs = [92.0] * 8 + [20.0] * 2

    report = compute_personalization_gain(
        episode_id="ses_gain_01",
        participant_id="part_gain",
        generic_observer_id="item_base_rate",
        generic_confidences=gen_confs,
        personalized_confidences=pers_confs,
        outcomes=outcomes,
        block_size=2,
        n_bootstrap=100,
        seed=42,
    )

    assert report.personalized_brier < report.generic_brier
    assert report.delta_brier_gain > 0.0  # Positive gain
    assert report.is_personalization_beneficial is True
    assert "Across the currently observed trials" in report.epistemic_statement
