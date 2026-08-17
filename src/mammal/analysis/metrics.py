"""First-order and metacognitive statistical metrics (Accuracy, Brier, Calibration, Type-2 SDT)."""

from __future__ import annotations

import math
from typing import Any, Sequence
import numpy as np
from scipy import stats


def compute_accuracy(outcomes: Sequence[bool]) -> float:
    """Compute first-order proportion correct."""
    if len(outcomes) == 0:
        return 0.0
    return float(np.mean([1.0 if x else 0.0 for x in outcomes]))


def compute_brier_score(confidences: Sequence[float], outcomes: Sequence[bool]) -> float:
    """Compute quadratic Brier loss between probability confidence in [0, 1] and binary outcome {0, 1}."""
    if len(confidences) != len(outcomes) or len(confidences) == 0:
        raise ValueError("Confidences and outcomes must be non-empty and of equal length.")

    # Normalize confidences to [0, 1]
    probs = np.array([c / 100.0 if c > 1.0 else c for c in confidences], dtype=float)
    targets = np.array([1.0 if y else 0.0 for y in outcomes], dtype=float)

    return float(np.mean((probs - targets) ** 2))


def compute_expected_calibration_error(
    confidences: Sequence[float],
    outcomes: Sequence[bool],
    n_bins: int = 10,
) -> tuple[float, list[dict[str, Any]]]:
    """Compute Expected Calibration Error (ECE) and reliability diagram bins."""
    if len(confidences) != len(outcomes) or len(confidences) == 0:
        raise ValueError("Confidences and outcomes must be non-empty and of equal length.")

    probs = np.array([c / 100.0 if c > 1.0 else c for c in confidences], dtype=float)
    targets = np.array([1.0 if y else 0.0 for y in outcomes], dtype=float)

    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    bins_data = []

    for i in range(n_bins):
        low, high = bin_edges[i], bin_edges[i + 1]
        if i == n_bins - 1:
            mask = (probs >= low) & (probs <= high)
        else:
            mask = (probs >= low) & (probs < high)

        count = int(np.sum(mask))
        if count > 0:
            bin_conf = float(np.mean(probs[mask]))
            bin_acc = float(np.mean(targets[mask]))
            weight = count / len(probs)
            ece += weight * abs(bin_acc - bin_conf)
            bins_data.append({
                "bin_index": i,
                "range": [float(low), float(high)],
                "count": count,
                "mean_confidence": round(bin_conf, 4),
                "mean_accuracy": round(bin_acc, 4),
                "calibration_gap": round(bin_acc - bin_conf, 4),
            })
        else:
            bins_data.append({
                "bin_index": i,
                "range": [float(low), float(high)],
                "count": 0,
                "mean_confidence": None,
                "mean_accuracy": None,
                "calibration_gap": None,
            })

    return float(ece), bins_data


def compute_auroc2(confidences: Sequence[float], outcomes: Sequence[bool]) -> float:
    """Compute Type-2 AUROC (area under Type-2 ROC curve) measuring metacognitive sensitivity."""
    if len(confidences) != len(outcomes) or len(confidences) == 0:
        raise ValueError("Confidences and outcomes must be non-empty and of equal length.")

    conf = np.array(confidences, dtype=float)
    targets = np.array([1 if y else 0 for y in outcomes], dtype=int)

    n_correct = int(np.sum(targets == 1))
    n_incorrect = int(np.sum(targets == 0))

    if n_correct == 0 or n_incorrect == 0:
        # Cannot compute ROC without both correct and incorrect trials
        return 0.5

    # Use Mann-Whitney U formulation for non-parametric AUROC
    correct_conf = conf[targets == 1]
    incorrect_conf = conf[targets == 0]

    u_stat, _ = stats.mannwhitneyu(correct_conf, incorrect_conf, alternative="greater")
    auroc2 = float(u_stat / (n_correct * n_incorrect))
    return float(np.clip(auroc2, 0.0, 1.0))


def compute_type2_sdt(
    confidences: Sequence[float],
    outcomes: Sequence[bool],
) -> dict[str, float]:
    """Compute first-order d' and empirical meta-d' approximation / metacognitive efficiency."""
    acc = compute_accuracy(outcomes)
    auroc2 = compute_auroc2(confidences, outcomes)

    # 1. First-order d' approximation for 2-alternative or multi-choice forced choice
    # Use standard log-linear correction to avoid infinite z-scores
    n = len(outcomes)
    n_correct = sum(1 if y else 0 for y in outcomes)
    p_hit = (n_correct + 0.5) / (n + 1.0)
    p_fa = 1.0 - p_hit
    d_prime = max(0.0, float(stats.norm.ppf(p_hit) - stats.norm.ppf(p_fa)))

    # 2. Meta-d' empirical baseline from Type-2 AUROC (Fleming & Lau 2014)
    # meta-d' ≈ sqrt(2) * norm.ppf(AUROC2)
    bounded_auroc = min(0.999, max(0.501, auroc2))
    meta_d_prime = float(math.sqrt(2.0) * stats.norm.ppf(bounded_auroc))

    # 3. Metacognitive efficiency M_ratio = meta_d' / d'
    m_ratio = float(meta_d_prime / d_prime) if d_prime > 0.05 else 1.0

    return {
        "accuracy": round(acc, 4),
        "auroc2": round(auroc2, 4),
        "d_prime": round(d_prime, 4),
        "meta_d_prime": round(meta_d_prime, 4),
        "m_ratio": round(m_ratio, 4),
    }
