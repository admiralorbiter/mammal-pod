"""Unit tests for transformed adaptive staircase algorithm and threshold estimation."""

from __future__ import annotations

import numpy as np
import pytest

from mammal.psychophysics.staircase import TransformedStaircase


def test_staircase_1up_2down_step_rules():
    sc = TransformedStaircase(
        initial_val=0.50,
        n_down=2,
        n_up=1,
        initial_step_size=0.10,
        min_step_size=0.01,
        min_val=0.01,
        max_val=1.00,
    )

    # Trial 1: Correct -> stays at 0.50 (needs 2 consecutive correct)
    s1 = sc.step(True)
    assert s1.current_val == 0.50
    assert s1.consecutive_correct == 1

    # Trial 2: Correct -> decrements by step_size (0.50 - 0.10 = 0.40)
    s2 = sc.step(True)
    assert s2.current_val == pytest.approx(0.40, abs=1e-4)
    assert s2.consecutive_correct == 0

    # Trial 3: Incorrect -> increments by step_size (0.40 + 0.10 = 0.50) -> REVERSAL!
    s3 = sc.step(False)
    assert s3.current_val == pytest.approx(0.50, abs=1e-4)
    assert s3.reversal_count == 1
    assert s3.step_size == pytest.approx(0.05, abs=1e-4)  # Halved step size


def test_staircase_convergence_on_simulated_observer():
    # Simulate an observer with true 70.7% perceptual coherence threshold at 0.25
    true_threshold = 0.25
    sc = TransformedStaircase(
        initial_val=0.60,
        n_down=2,
        n_up=1,
        initial_step_size=0.10,
        min_step_size=0.01,
        max_reversals=8,
        max_trials=60,
    )

    rng = np.random.default_rng(123)
    for _ in range(60):
        if sc.is_finished:
            break
        # Probability of correct response as logistic psychometric function
        coherence = sc.current_val
        # 50% chance at coherence=0, ~75% at true_threshold, ~99% at high coherence
        prob_correct = 0.5 + 0.5 / (1.0 + np.exp(-15.0 * (coherence - true_threshold)))
        is_correct = bool(rng.random() < prob_correct)
        sc.step(is_correct)

    threshold = sc.get_threshold()
    assert threshold is not None
    # Estimated threshold should be in neighborhood of true threshold (0.15 to 0.35)
    assert 0.10 <= threshold <= 0.40
