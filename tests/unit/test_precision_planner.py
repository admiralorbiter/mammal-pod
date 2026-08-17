"""Unit tests for simulation-based precision planning and sample size recommendation."""

from __future__ import annotations

import pytest

from mammal.analysis.precision_planner import plan_session_precision


def test_plan_session_precision_brier():
    res = plan_session_precision(
        target_metric="brier",
        target_ci_half_width=0.06,
        candidate_sample_sizes=[20, 50, 100, 200],
        n_simulations=200,
        seed=101,
    )

    assert res.target_metric == "brier"
    assert len(res.recommendations) == 4
    # Standard error should decrease monotonically with sample size
    ses = [r.standard_error for r in res.recommendations]
    assert ses[0] > ses[1] > ses[2] > ses[3]
    # Recommended sample size should be one of the candidate sizes
    assert res.recommended_sample_size in [20, 50, 100, 200]


def test_plan_session_precision_accuracy():
    res = plan_session_precision(
        target_metric="accuracy",
        target_ci_half_width=0.08,
        candidate_sample_sizes=[30, 60, 120, 200],
        n_simulations=150,
        seed=202,
    )

    assert res.target_metric == "accuracy"
    assert res.recommended_sample_size > 0
    assert any(r.meets_criterion for r in res.recommendations)


def test_plan_session_precision_auroc2():
    res = plan_session_precision(
        target_metric="auroc2",
        target_ci_half_width=0.10,
        candidate_sample_sizes=[40, 80, 160],
        n_simulations=100,
        seed=303,
    )

    assert res.target_metric == "auroc2"
    assert len(res.recommendations) == 3


def test_plan_session_precision_invalid_metric():
    with pytest.raises(ValueError, match="Unsupported target metric"):
        plan_session_precision(target_metric="invalid_metric", n_simulations=10)
