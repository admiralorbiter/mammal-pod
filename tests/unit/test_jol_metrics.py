"""Unit tests for Judgment of Learning (JOL) metrics and Goodman-Kruskal Gamma correlation."""

from __future__ import annotations

import pytest

from mammal.memory.metrics import (
    compute_gamma_correlation,
    compute_prospective_memory_metrics,
)


def test_gamma_correlation_perfect_concordance():
    # When JOL ordering perfectly matches recall ordering
    jol = [90.0, 80.0, 70.0, 30.0, 20.0]
    rec = [True, True, True, False, False]
    gamma = compute_gamma_correlation(jol, rec)
    assert gamma == 1.0


def test_gamma_correlation_perfect_discordance():
    # When higher JOL items are forgotten and lower JOL items are remembered
    jol = [90.0, 80.0, 20.0, 10.0]
    rec = [False, False, True, True]
    gamma = compute_gamma_correlation(jol, rec)
    assert gamma == -1.0


def test_compute_prospective_memory_metrics():
    jol = [85.0, 75.0, 40.0, 30.0]
    rec = [True, True, False, False]
    res = compute_prospective_memory_metrics(jol, rec)

    assert res["total_trials"] == 4.0
    assert res["recall_accuracy"] == 0.50
    assert res["mean_jol"] == pytest.approx(57.5, abs=0.1)
    assert res["gamma_correlation"] == 1.0
    assert res["prospective_auroc"] == 1.0
    assert res["prospective_brier_score"] < 0.15
