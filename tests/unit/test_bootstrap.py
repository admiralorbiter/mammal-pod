"""Unit tests for block bootstrap confidence interval estimation."""

from __future__ import annotations

import numpy as np
import pytest

from mammal.analysis.bootstrap import block_bootstrap_ci


def test_block_bootstrap_ci_basic_properties():
    # Simple list of binary responses
    data = [{"is_correct": True if i % 2 == 0 else False} for i in range(20)]

    def calc_mean(sample):
        return np.mean([1.0 if x["is_correct"] else 0.0 for x in sample])

    pt, low, high = block_bootstrap_ci(data, calc_mean, block_size=4, n_resamples=200, seed=123)

    assert pt == 0.5
    assert 0.0 <= low <= pt
    assert pt <= high <= 1.0


def test_block_bootstrap_small_sample():
    data = [{"val": 1.0}]
    pt, low, high = block_bootstrap_ci(data, lambda s: s[0]["val"])
    assert pt == 1.0
    assert low == 1.0
    assert high == 1.0
