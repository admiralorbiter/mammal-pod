"""Intervention effects analysis disentangling feedback-induced shifts from pre-existing traits (AGENTS.md Rule 6)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import numpy as np
from sqlalchemy.orm import Session

from mammal.analysis.metrics import (
    compute_accuracy,
    compute_brier_score,
    compute_expected_calibration_error,
)
from mammal.models.entities import Trial, TrialEvent


@dataclass
class InterventionEffectReport:
    """Quantitative comparison of baseline vs. post-intervention participant behavior."""

    episode_id: str
    baseline_trials_count: int
    intervention_trials_count: int
    baseline_accuracy: float
    intervention_accuracy: float
    baseline_ece: float
    intervention_ece: float
    delta_ece_improvement: float  # ECE_baseline - ECE_intervention (positive = calibration improved)
    baseline_brier: float
    intervention_brier: float
    delta_brier_improvement: float  # Brier_baseline - Brier_intervention (positive = loss reduced)
    rule6_epistemic_warning: str


def compute_intervention_effects(
    session: Session,
    episode_id: str,
) -> InterventionEffectReport:
    """Analyze behavioral differences between unassisted baseline trials and intervention trials."""
    trials = (
        session.query(Trial)
        .filter(Trial.episode_id == episode_id)
        .order_by(Trial.trial_index.asc())
        .all()
    )

    events = (
        session.query(TrialEvent)
        .filter(TrialEvent.episode_id == episode_id)
        .all()
    )
    intervention_trial_ids = {
        e.trial_id for e in events if e.event_type == "intervention.delivered"
    }

    base_confs: list[float] = []
    base_outcomes: list[bool] = []
    interv_confs: list[float] = []
    interv_outcomes: list[bool] = []

    for t in trials:
        if t.outcome is None:
            continue

        conf = t.confidence.value if t.confidence else 75.0
        corr = t.outcome.is_correct

        if t.id in intervention_trial_ids:
            interv_confs.append(conf)
            interv_outcomes.append(corr)
        else:
            base_confs.append(conf)
            base_outcomes.append(corr)

    if not base_outcomes or not interv_outcomes:
        raise ValueError(
            f"Episode {episode_id} must have both baseline and intervention trials to compute effects. "
            f"Found {len(base_outcomes)} baseline and {len(interv_outcomes)} intervention trials."
        )

    # Compute estimands for baseline
    b_acc = compute_accuracy(base_outcomes)
    b_ece, _ = compute_expected_calibration_error(base_confs, base_outcomes)
    b_brier = compute_brier_score(base_confs, base_outcomes)

    # Compute estimands for intervention
    i_acc = compute_accuracy(interv_outcomes)
    i_ece, _ = compute_expected_calibration_error(interv_confs, interv_outcomes)
    i_brier = compute_brier_score(interv_confs, interv_outcomes)

    delta_ece = b_ece - i_ece
    delta_brier = b_brier - i_brier

    rule6_warning = (
        "MAMMAL Epistemic Notice (AGENTS.md Rule 6): Intervention-produced behavior reflects "
        "interaction with model feedback and must NEVER be treated as independent evidence of "
        "a participant's pre-existing unassisted cognitive traits."
    )

    return InterventionEffectReport(
        episode_id=episode_id,
        baseline_trials_count=len(base_outcomes),
        intervention_trials_count=len(interv_outcomes),
        baseline_accuracy=round(b_acc, 4),
        intervention_accuracy=round(i_acc, 4),
        baseline_ece=round(b_ece, 4),
        intervention_ece=round(i_ece, 4),
        delta_ece_improvement=round(delta_ece, 4),
        baseline_brier=round(b_brier, 4),
        intervention_brier=round(i_brier, 4),
        delta_brier_improvement=round(delta_brier, 4),
        rule6_epistemic_warning=rule6_warning,
    )
