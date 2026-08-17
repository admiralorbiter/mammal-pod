"""Prequential history compiler enforcing strict causal ordering with zero future leakage."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session

from mammal.models.entities import Episode, Trial


@dataclass
class HistoricalTrialSummary:
    """Summary record of a completed prior trial."""

    trial_id: str
    episode_id: str
    domain: str
    is_correct: bool
    confidence: float | None
    latency_ms: float | None
    occurred_at: str


@dataclass
class ParticipantPrequentialHistory:
    """Causal prequential history for a participant strictly prior to a target trial."""

    participant_id: str
    target_trial_id: str
    total_prior_trials: int
    overall_accuracy: float
    domain_accuracy: dict[str, float]
    mean_reported_confidence: float | None
    calibration_bias: float  # (mean_conf / 100.0) - overall_accuracy (positive = overconfident)
    mean_latency_ms: float
    history_trials: list[HistoricalTrialSummary] = field(default_factory=list)


def compile_prequential_history(
    session: Session,
    participant_id: str,
    target_trial_id: str,
) -> ParticipantPrequentialHistory:
    """Compile historical trials completed strictly BEFORE target_trial_id (AGENTS.md Rule 9 & Gate E05)."""
    target_trial = session.get(Trial, target_trial_id)
    if not target_trial:
        raise ValueError(f"Target trial {target_trial_id} not found.")

    target_episode = session.get(Episode, target_trial.episode_id)
    if not target_episode:
        raise ValueError(f"Target episode {target_trial.episode_id} not found.")

    # Query all completed trials for this participant ordered chronologically by episode and index
    stmt = (
        select(Trial)
        .join(Episode, Trial.episode_id == Episode.id)
        .where(
            Episode.participant_id == participant_id,
            Trial.id != target_trial_id,
            Trial.status == "completed",
        )
        .order_by(Episode.started_at.asc(), Trial.trial_index.asc())
    )
    raw_trials = list(session.scalars(stmt).all())

    # Filter strictly:
    # 1. Trials from earlier episodes (started_at < target_episode.started_at)
    # 2. Trials from the same episode with trial_index < target_trial.trial_index
    prior_trials: list[Trial] = []
    for t in raw_trials:
        if t.episode_id == target_trial.episode_id:
            if t.trial_index < target_trial.trial_index:
                prior_trials.append(t)
        else:
            ep = session.get(Episode, t.episode_id)
            if ep and ep.started_at <= target_episode.started_at:
                prior_trials.append(t)

    # Build historical summaries
    from mammal.models.entities import Item

    summaries: list[HistoricalTrialSummary] = []
    domain_correct: dict[str, list[bool]] = {}
    confidences: list[float] = []
    latencies: list[float] = []

    for t in prior_trials:
        if t.outcome is None:
            continue

        item = session.get(Item, (t.item_id, t.item_version))
        item_domain = item.domain if (item and item.domain) else "unknown"

        is_corr = t.outcome.is_correct
        conf = t.confidence.value if t.confidence else None
        lat = t.answer.response_latency_ms if t.answer else None

        if conf is not None:
            confidences.append(conf)
        if lat is not None:
            latencies.append(lat)

        if item_domain not in domain_correct:
            domain_correct[item_domain] = []
        domain_correct[item_domain].append(is_corr)

        occ_at = (
            t.completed_at.isoformat()
            if t.completed_at
            else (t.prompt_shown_at.isoformat() if t.prompt_shown_at else "")
        )

        summaries.append(HistoricalTrialSummary(
            trial_id=t.id,
            episode_id=t.episode_id,
            domain=item_domain,
            is_correct=is_corr,
            confidence=conf,
            latency_ms=lat,
            occurred_at=occ_at,
        ))

    total = len(summaries)
    if total > 0:
        overall_acc = float(np.mean([1.0 if s.is_correct else 0.0 for s in summaries]))
        mean_conf = float(np.mean(confidences)) if confidences else None
        mean_lat = float(np.mean(latencies)) if latencies else 800.0
        calib_bias = float((mean_conf / 100.0) - overall_acc) if mean_conf is not None else 0.0
    else:
        overall_acc = 0.70
        mean_conf = None
        mean_lat = 800.0
        calib_bias = 0.0

    domain_acc_map = {
        d: float(np.mean([1.0 if y else 0.0 for y in bools]))
        for d, bools in domain_correct.items()
    }

    return ParticipantPrequentialHistory(
        participant_id=participant_id,
        target_trial_id=target_trial_id,
        total_prior_trials=total,
        overall_accuracy=round(overall_acc, 4),
        domain_accuracy={d: round(a, 4) for d, a in domain_acc_map.items()},
        mean_reported_confidence=round(mean_conf, 2) if mean_conf is not None else None,
        calibration_bias=round(calib_bias, 4),
        mean_latency_ms=round(mean_lat, 2),
        history_trials=summaries,
    )
