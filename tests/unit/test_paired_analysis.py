"""Unit tests for paired comparisons and Participant Advantage Index (PAI)."""

from __future__ import annotations

import pytest

from mammal.analysis.paired import compute_paired_comparison


def test_paired_comparison_human_superiority():
    # Human has high confidence on correct trials, low on incorrect
    # Observer has flat 50% confidence (uniform guesser)
    outcomes = [True] * 8 + [False] * 2  # 80% accuracy
    self_conf = [90.0] * 8 + [20.0] * 2
    obs_conf = [50.0] * 10

    res = compute_paired_comparison(
        episode_id="ses_paired_test",
        observer_id="uniform_chance",
        self_confidences=self_conf,
        observer_confidences=obs_conf,
        outcomes=outcomes,
        block_size=2,
        n_bootstrap=100,
        seed=42,
    )

    assert res.self_brier < res.observer_brier
    assert res.delta_brier > 0.0  # Positive delta means Self is better
    assert res.participant_advantage_index > 0.0
    assert res.self_auroc2 == 1.0  # Perfect discrimination for Self
    assert res.delta_auroc2 > 0.0


def test_paired_comparison_equal_performance():
    outcomes = [True, False, True, False]
    conf = [70.0, 40.0, 70.0, 40.0]

    res = compute_paired_comparison(
        episode_id="ses_equal_test",
        observer_id="mirror_observer",
        self_confidences=conf,
        observer_confidences=conf,
        outcomes=outcomes,
        n_bootstrap=50,
        seed=1,
    )

    assert res.delta_brier == pytest.approx(0.0, abs=1e-4)
    assert res.participant_advantage_index == pytest.approx(0.0, abs=1e-4)
    assert res.delta_auroc2 == pytest.approx(0.0, abs=1e-4)
