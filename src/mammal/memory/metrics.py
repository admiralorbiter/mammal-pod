"""Prospective memory resolution and Judgment of Learning (JOL) estimands."""

from __future__ import annotations

from typing import Sequence
import numpy as np

from mammal.analysis.metrics import compute_auroc2, compute_brier_score


def compute_gamma_correlation(
    jol_ratings: Sequence[float],
    recall_outcomes: Sequence[bool],
) -> float:
    """Compute Goodman-Kruskal Gamma correlation between prospective JOLs and future recall outcomes.

    Gamma = (C - D) / (C + D), where C is concordant pairs and D is discordant pairs.
    Ties in either JOL or Recall are excluded. Range: [-1.0, +1.0].
    """
    n = len(recall_outcomes)
    if len(jol_ratings) != n or n < 2:
        return 0.0

    c = 0
    d = 0

    j_arr = np.array(jol_ratings, dtype=float)
    r_arr = np.array(recall_outcomes, dtype=int)

    for i in range(n):
        for j in range(i + 1, n):
            j_diff = j_arr[i] - j_arr[j]
            r_diff = r_arr[i] - r_arr[j]

            # If either variable is tied, the pair is ignored in Gamma
            if j_diff == 0.0 or r_diff == 0:
                continue

            if (j_diff > 0 and r_diff > 0) or (j_diff < 0 and r_diff < 0):
                c += 1
            else:
                d += 1

    if (c + d) == 0:
        return 0.0

    return float(round((c - d) / (c + d), 4))


def compute_prospective_memory_metrics(
    jol_ratings: Sequence[float],
    recall_outcomes: Sequence[bool],
) -> dict[str, float]:
    """Compute gold-standard prospective metacognitive estimands for future memory."""
    n = len(recall_outcomes)
    if len(jol_ratings) != n or n == 0:
        raise ValueError("JOL ratings and recall outcomes must be of equal non-zero length.")

    acc = float(np.mean([1.0 if y else 0.0 for y in recall_outcomes]))
    mean_jol = float(np.mean(jol_ratings))
    gamma = compute_gamma_correlation(jol_ratings, recall_outcomes)
    brier = compute_brier_score(jol_ratings, recall_outcomes)
    auroc = compute_auroc2(jol_ratings, recall_outcomes)

    return {
        "total_trials": float(n),
        "recall_accuracy": round(acc, 4),
        "mean_jol": round(mean_jol, 2),
        "gamma_correlation": round(gamma, 4),
        "prospective_brier_score": round(brier, 4),
        "prospective_auroc": round(auroc, 4),
    }
