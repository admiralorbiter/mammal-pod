"""Unit tests for statistical estimands, calibration, Brier score, and Type-2 SDT metrics."""

from __future__ import annotations

import math
import pytest

from mammal.analysis.metrics import (
    compute_accuracy,
    compute_auroc2,
    compute_brier_score,
    compute_expected_calibration_error,
    compute_type2_sdt,
)


def test_accuracy_computation():
    assert compute_accuracy([]) == 0.0
    assert compute_accuracy([True, True, True, True]) == 1.0
    assert compute_accuracy([True, False, True, False]) == 0.5
    assert compute_accuracy([False, False, False]) == 0.0


def test_brier_score_properties():
    # 1. Perfect confidence on correct and incorrect
    assert compute_brier_score([1.0, 0.0], [True, False]) == 0.0
    assert compute_brier_score([100.0, 0.0], [True, False]) == 0.0

    # 2. Complete reverse confidence (maximum loss)
    assert compute_brier_score([0.0, 1.0], [True, False]) == 1.0

    # 3. 50% random guessing on equal outcomes
    assert compute_brier_score([50.0, 50.0], [True, False]) == 0.25


def test_expected_calibration_error():
    # 1. Perfectly calibrated items (100% confidence when right, 0% when wrong)
    conf = [100.0, 100.0, 0.0, 0.0]
    outcomes = [True, True, False, False]
    ece, bins = compute_expected_calibration_error(conf, outcomes, n_bins=5)
    assert ece == pytest.approx(0.0, abs=1e-4)

    # 2. Overconfident items (100% confidence, but 50% accuracy)
    conf_over = [100.0, 100.0, 100.0, 100.0]
    outcomes_half = [True, False, True, False]
    ece_over, _ = compute_expected_calibration_error(conf_over, outcomes_half, n_bins=5)
    assert ece_over == pytest.approx(0.5, abs=1e-4)


def test_auroc2_metacognitive_sensitivity():
    # 1. Perfect metacognition: higher confidence always on correct trials
    conf_perfect = [90.0, 85.0, 80.0, 30.0, 20.0]
    outcomes_perfect = [True, True, True, False, False]
    assert compute_auroc2(conf_perfect, outcomes_perfect) == 1.0

    # 2. Chance metacognition: confidence independent of accuracy
    conf_chance = [50.0, 50.0, 50.0, 50.0]
    outcomes_chance = [True, True, False, False]
    assert compute_auroc2(conf_chance, outcomes_chance) == 0.5

    # 3. Inverse / blindsight-like metacognition
    conf_inv = [20.0, 10.0, 90.0, 80.0]
    outcomes_inv = [True, True, False, False]
    assert compute_auroc2(conf_inv, outcomes_inv) == 0.0


def test_type2_sdt_metrics():
    conf = [90.0, 85.0, 80.0, 75.0, 70.0, 30.0]
    outcomes = [True, True, True, True, True, False]
    sdt = compute_type2_sdt(conf, outcomes)

    assert "accuracy" in sdt
    assert "auroc2" in sdt
    assert "d_prime" in sdt
    assert "meta_d_prime" in sdt
    assert "m_ratio" in sdt
    assert sdt["accuracy"] == pytest.approx(5 / 6, abs=1e-3)
    assert sdt["auroc2"] == 1.0
    assert sdt["d_prime"] > 0.0
    assert sdt["meta_d_prime"] > 0.0
