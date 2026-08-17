"""Personalization gain analysis comparing generic vs. prequential personalized observers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import numpy as np

from mammal.analysis.metrics import compute_auroc2, compute_brier_score


@dataclass
class PersonalizationGainReport:
    """Statistical evaluation of whether participant history improves prediction over generic baselines (Gate E05)."""

    episode_id: str
    participant_id: str
    total_trials: int
    generic_observer_id: str
    generic_brier: float
    personalized_brier: float
    delta_brier_gain: float  # Brier_Generic - Brier_Personalized (positive = personalization improved)
    delta_brier_gain_ci: tuple[float, float]
    generic_auroc2: float
    personalized_auroc2: float
    delta_auroc2_gain: float  # AUROC2_Personalized - AUROC2_Generic
    delta_auroc2_gain_ci: tuple[float, float]
    is_personalization_beneficial: bool
    epistemic_statement: str


def compute_personalization_gain(
    episode_id: str,
    participant_id: str,
    generic_observer_id: str,
    generic_confidences: Sequence[float],
    personalized_confidences: Sequence[float],
    outcomes: Sequence[bool],
    block_size: int = 4,
    n_bootstrap: int = 500,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> PersonalizationGainReport:
    """Compute Personalization Gain with session-preserving block bootstrap empirical 95% CIs."""
    n = len(outcomes)
    if len(generic_confidences) != n or len(personalized_confidences) != n or n == 0:
        raise ValueError("Generic confidences, personalized confidences, and outcomes must be of equal non-zero length.")

    # 1. Point estimates
    gen_brier = compute_brier_score(generic_confidences, outcomes)
    pers_brier = compute_brier_score(personalized_confidences, outcomes)
    delta_brier = gen_brier - pers_brier

    gen_auroc = compute_auroc2(generic_confidences, outcomes)
    pers_auroc = compute_auroc2(personalized_confidences, outcomes)
    delta_auroc = pers_auroc - gen_auroc

    # 2. Block bootstrap resampling
    rng = np.random.default_rng(seed)
    n_blocks = max(1, int(np.ceil(n / block_size)))
    block_indices = [list(range(i * block_size, min((i + 1) * block_size, n))) for i in range(n_blocks)]

    boot_delta_briers: list[float] = []
    boot_delta_aurocs: list[float] = []

    g_conf = np.array(generic_confidences, dtype=float)
    p_conf = np.array(personalized_confidences, dtype=float)
    y_arr = np.array(outcomes, dtype=bool)

    for _ in range(n_bootstrap):
        sampled_block_idx = rng.choice(len(block_indices), size=n_blocks, replace=True)
        sample_indices = []
        for b_idx in sampled_block_idx:
            sample_indices.extend(block_indices[b_idx])
        sample_indices = sample_indices[:n]

        sub_g = g_conf[sample_indices]
        sub_p = p_conf[sample_indices]
        sub_y = y_arr[sample_indices]

        try:
            b_g = compute_brier_score(sub_g, sub_y)
            b_p = compute_brier_score(sub_p, sub_y)
            a_g = compute_auroc2(sub_g, sub_y)
            a_p = compute_auroc2(sub_p, sub_y)

            boot_delta_briers.append(b_g - b_p)
            boot_delta_aurocs.append(a_p - a_g)
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

    is_beneficial = delta_brier > 0.0 and ci_db[0] > -0.05

    # AGENTS.md Rule 5 phrasing
    epistemic_stmt = (
        f"Across the currently observed trials for participant {participant_id}, the model estimates "
        f"a personalization Brier gain of \u0394 = {delta_brier:+.4f} (95% CI [{ci_db[0]:+.4f}, {ci_db[1]:+.4f}]) "
        f"and metacognitive sensitivity shift of \u0394 AUROC2 = {delta_auroc:+.4f}."
    )

    return PersonalizationGainReport(
        episode_id=episode_id,
        participant_id=participant_id,
        total_trials=n,
        generic_observer_id=generic_observer_id,
        generic_brier=round(gen_brier, 4),
        personalized_brier=round(pers_brier, 4),
        delta_brier_gain=round(delta_brier, 4),
        delta_brier_gain_ci=ci_db,
        generic_auroc2=round(gen_auroc, 4),
        personalized_auroc2=round(pers_auroc, 4),
        delta_auroc2_gain=round(delta_auroc, 4),
        delta_auroc2_gain_ci=ci_da,
        is_personalization_beneficial=is_beneficial,
        epistemic_statement=epistemic_stmt,
    )
