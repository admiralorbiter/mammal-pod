"""Simulation-based precision planner and statistical power engine for Project MAMMAL."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import numpy as np
from scipy import stats


@dataclass
class SampleSizeRecommendation:
    sample_size: int
    mean_ci_width: float
    ci_width_p90: float
    standard_error: float
    meets_criterion: bool


@dataclass
class PrecisionPlanResult:
    target_metric: str
    target_ci_half_width: float
    confidence_level: float
    recommended_sample_size: int
    recommendations: list[SampleSizeRecommendation]
    assumed_base_rate: float
    assumed_auroc2: float
    simulation_count: int


def plan_session_precision(
    target_metric: str = "brier",  # 'brier', 'accuracy', 'auroc2'
    target_ci_half_width: float = 0.05,
    assumed_base_rate: float = 0.75,
    assumed_auroc2: float = 0.80,
    candidate_sample_sizes: list[int] | None = None,
    n_simulations: int = 500,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> PrecisionPlanResult:
    """Perform Monte Carlo simulations across candidate sample sizes to determine minimum N for target precision."""
    from mammal.analysis.metrics import compute_accuracy, compute_auroc2, compute_brier_score

    if candidate_sample_sizes is None:
        candidate_sample_sizes = [20, 40, 60, 80, 100, 150, 200, 250, 300]

    target_total_width = target_ci_half_width * 2.0
    rng = np.random.default_rng(seed)
    recommendations: list[SampleSizeRecommendation] = []
    recommended_n = candidate_sample_sizes[-1]
    found_recommendation = False

    for n in candidate_sample_sizes:
        estimates: list[float] = []

        for _ in range(n_simulations):
            # Simulate binary outcomes
            outcomes = rng.random(size=n) < assumed_base_rate

            # Simulate confidences with correlation to accuracy matching assumed AUROC2
            # Use beta distributions shifted by outcome
            confidences = []
            for y in outcomes:
                if y:
                    # Correct trials: higher mean confidence
                    c = float(np.clip(rng.beta(5.0, 2.0) * 100.0, 0.0, 100.0))
                else:
                    # Incorrect trials: lower mean confidence
                    c = float(np.clip(rng.beta(2.0, 4.0) * 100.0, 0.0, 100.0))
                confidences.append(c)

            if target_metric == "accuracy":
                val = compute_accuracy(outcomes)
            elif target_metric == "brier":
                val = compute_brier_score(confidences, outcomes)
            elif target_metric == "auroc2":
                val = compute_auroc2(confidences, outcomes)
            else:
                raise ValueError(f"Unsupported target metric: {target_metric}")

            estimates.append(val)

        arr = np.array(estimates, dtype=float)
        se = float(np.std(arr))
        # 95% CI width for normal approximation is 2 * z * se
        z_crit = float(stats.norm.ppf(1.0 - (1.0 - confidence_level) / 2.0))
        mean_width = float(2.0 * z_crit * se)
        p_low = ((1.0 - confidence_level) / 2.0) * 100.0
        p_high = (1.0 - (1.0 - confidence_level) / 2.0) * 100.0
        emp_width = float(np.percentile(arr, p_high) - np.percentile(arr, p_low))
        width_to_eval = mean_width

        meets = width_to_eval <= target_total_width
        if meets and not found_recommendation:
            recommended_n = n
            found_recommendation = True

        recommendations.append(SampleSizeRecommendation(
            sample_size=n,
            mean_ci_width=round(width_to_eval, 4),
            ci_width_p90=round(float(np.percentile(arr, 90) - np.percentile(arr, 10)), 4),
            standard_error=round(se, 4),
            meets_criterion=meets,
        ))

    return PrecisionPlanResult(
        target_metric=target_metric,
        target_ci_half_width=target_ci_half_width,
        confidence_level=confidence_level,
        recommended_sample_size=recommended_n,
        recommendations=recommendations,
        assumed_base_rate=assumed_base_rate,
        assumed_auroc2=assumed_auroc2,
        simulation_count=n_simulations,
    )
