"""Paired statistical comparison and Participant Advantage Index (PAI) engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import numpy as np

from mammal.analysis.metrics import compute_auroc2, compute_brier_score


@dataclass
class PairedComparisonResult:
    """Paired evaluation of Human Self vs. External Observer model."""

    episode_id: str
    observer_id: str
    total_trials: int
    self_brier: float
    observer_brier: float
    delta_brier: float  # Brier_Observer - Brier_Self (positive means Self has lower error)
    delta_brier_ci: tuple[float, float]
    self_auroc2: float
    observer_auroc2: float
    delta_auroc2: float  # AUROC2_Self - AUROC2_Observer (positive means Self has higher sensitivity)
    delta_auroc2_ci: tuple[float, float]
    participant_advantage_index: float  # (Brier_Observer - Brier_Self) / Brier_Observer
    pai_ci: tuple[float, float]


def compute_paired_comparison(
    episode_id: str,
    observer_id: str,
    self_confidences: Sequence[float],
    observer_confidences: Sequence[float],
    outcomes: Sequence[bool],
    block_size: int = 4,
    n_bootstrap: int = 500,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> PairedComparisonResult:
    """Compute paired comparison metrics with session-preserving block bootstrap empirical 95% CIs."""
    n = len(outcomes)
    if len(self_confidences) != n or len(observer_confidences) != n or n == 0:
        raise ValueError("Self confidences, observer confidences, and outcomes must be of equal non-zero length.")

    # 1. Point estimates
    self_brier = compute_brier_score(self_confidences, outcomes)
    obs_brier = compute_brier_score(observer_confidences, outcomes)
    delta_brier = obs_brier - self_brier

    self_auroc = compute_auroc2(self_confidences, outcomes)
    obs_auroc = compute_auroc2(observer_confidences, outcomes)
    delta_auroc = self_auroc - obs_auroc

    pai = (obs_brier - self_brier) / obs_brier if obs_brier > 1e-6 else 0.0

    # 2. Block bootstrap resampling
    rng = np.random.default_rng(seed)
    n_blocks = max(1, int(np.ceil(n / block_size)))
    block_indices = [list(range(i * block_size, min((i + 1) * block_size, n))) for i in range(n_blocks)]

    boot_delta_briers: list[float] = []
    boot_delta_aurocs: list[float] = []
    boot_pais: list[float] = []

    s_conf = np.array(self_confidences, dtype=float)
    o_conf = np.array(observer_confidences, dtype=float)
    y_arr = np.array(outcomes, dtype=bool)

    for _ in range(n_bootstrap):
        sampled_block_idx = rng.choice(len(block_indices), size=n_blocks, replace=True)
        sample_indices = []
        for b_idx in sampled_block_idx:
            sample_indices.extend(block_indices[b_idx])
        sample_indices = sample_indices[:n]

        sub_s_conf = s_conf[sample_indices]
        sub_o_conf = o_conf[sample_indices]
        sub_y = y_arr[sample_indices]

        try:
            b_s = compute_brier_score(sub_s_conf, sub_y)
            b_o = compute_brier_score(sub_o_conf, sub_y)
            db = b_o - b_s
            p_idx = (b_o - b_s) / b_o if b_o > 1e-6 else 0.0

            a_s = compute_auroc2(sub_s_conf, sub_y)
            a_o = compute_auroc2(sub_o_conf, sub_y)
            da = a_s - a_o

            boot_delta_briers.append(db)
            boot_delta_aurocs.append(da)
            boot_pais.append(p_idx)
        except Exception:
            continue

    p_low = ((1.0 - confidence_level) / 2.0) * 100.0
    p_high = (1.0 - (1.0 - confidence_level) / 2.0) * 100.0

    if boot_delta_briers:
        ci_db = (
            round(float(np.percentile(boot_delta_briers, p_low)), 4),
            round(float(np.percentile(boot_delta_briers, p_high)), 4),
        )
    else:
        ci_db = (round(delta_brier, 4), round(delta_brier, 4))

    if boot_delta_aurocs:
        ci_da = (
            round(float(np.percentile(boot_delta_aurocs, p_low)), 4),
            round(float(np.percentile(boot_delta_aurocs, p_high)), 4),
        )
    else:
        ci_da = (round(delta_auroc, 4), round(delta_auroc, 4))

    if boot_pais:
        ci_pai = (
            round(float(np.percentile(boot_pais, p_low)), 4),
            round(float(np.percentile(boot_pais, p_high)), 4),
        )
    else:
        ci_pai = (round(pai, 4), round(pai, 4))

    return PairedComparisonResult(
        episode_id=episode_id,
        observer_id=observer_id,
        total_trials=n,
        self_brier=round(self_brier, 4),
        observer_brier=round(obs_brier, 4),
        delta_brier=round(delta_brier, 4),
        delta_brier_ci=ci_db,
        self_auroc2=round(self_auroc, 4),
        observer_auroc2=round(obs_auroc, 4),
        delta_auroc2=round(delta_auroc, 4),
        delta_auroc2_ci=ci_da,
        participant_advantage_index=round(pai, 4),
        pai_ci=ci_pai,
    )
