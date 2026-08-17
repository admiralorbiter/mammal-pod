"""Controlled intervention delivery engine and crossover trial assignment (AGENTS.md Rule 6)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from sqlalchemy.orm import Session

from mammal.events.engine import EventEngine
from mammal.interventions.governance import InterventionGovernanceGuard
from mammal.models.entities import Episode, Trial


class FeedbackCondition(str, Enum):
    """Controlled experimental feedback conditions."""

    NO_FEEDBACK = "no_feedback"
    ITEM_CORRECTNESS = "item_correctness"
    MODEL_DISCLOSURE = "model_disclosure"
    CALIBRATION_COACHING = "calibration_coaching"


@dataclass
class InterventionDeliveryRecord:
    """Provenance record of an experimental intervention delivered to a participant."""

    intervention_id: str
    episode_id: str
    trial_id: str
    condition: str
    source_model: str
    source_version: str
    evidence_basis: str
    content_text: str
    delivered_at: str


class CrossoverBlockAssigner:
    """Randomized and Latin-square crossover block scheduler for intervention studies."""

    @staticmethod
    def assign_aba_crossover(
        n_blocks: int,
        intervention_condition: FeedbackCondition = FeedbackCondition.MODEL_DISCLOSURE,
    ) -> list[FeedbackCondition]:
        """Assign ABA (Baseline-Intervention-Baseline) or ABAB crossover sequence."""
        schedule: list[FeedbackCondition] = []
        for b in range(n_blocks):
            if b % 2 == 1:
                schedule.append(intervention_condition)
            else:
                schedule.append(FeedbackCondition.NO_FEEDBACK)
        return schedule

    @staticmethod
    def assign_latin_square(
        participant_index: int,
        conditions: list[FeedbackCondition],
    ) -> list[FeedbackCondition]:
        """Generate balanced Latin-square permutation for a participant index."""
        k = len(conditions)
        if k == 0:
            return []
        shift = participant_index % k
        return conditions[shift:] + conditions[:shift]


def deliver_intervention(
    session: Session,
    episode_id: str,
    trial_id: str,
    condition: FeedbackCondition,
    message: str,
    source_model: str = "mantis_v1",
    source_version: str = "1.0.0",
    evidence_basis: str = "empirical_prequential_history",
) -> InterventionDeliveryRecord:
    """Validate and log a controlled intervention event under AGENTS.md Rule 6 governance."""
    episode = session.get(Episode, episode_id)
    if not episode:
        raise ValueError(f"Episode {episode_id} not found.")

    # 1. Audit against safety & Rule 5/6 governance
    check = InterventionGovernanceGuard.validate_intervention(
        message=message,
        session_mode=episode.mode,
        protocol_allows_feedback=(episode.mode == "intervention"),
    )
    if not check.is_approved:
        err_msg = "; ".join(check.violations)
        raise PermissionError(f"Intervention governance rejected message: {err_msg}")

    event_engine = EventEngine(session)

    # 2. Record intervention.decision_point event
    event_engine.record_event(
        trial_id=trial_id,
        episode_id=episode_id,
        event_type="intervention.decision_point",
        actor=f"model:{source_model}",
        payload={
            "condition": condition.value,
            "source_model": source_model,
            "source_version": source_version,
            "evidence_basis": evidence_basis,
        },
    )

    # 3. Record intervention.delivered event
    event = event_engine.record_event(
        trial_id=trial_id,
        episode_id=episode_id,
        event_type="intervention.delivered",
        actor=f"model:{source_model}",
        payload={
            "condition": condition.value,
            "content_text": check.sanitized_message,
            "source_model": source_model,
            "source_version": source_version,
        },
    )

    session.commit()

    return InterventionDeliveryRecord(
        intervention_id=event.event_id,
        episode_id=episode_id,
        trial_id=trial_id,
        condition=condition.value,
        source_model=source_model,
        source_version=source_version,
        evidence_basis=evidence_basis,
        content_text=check.sanitized_message,
        delivered_at=event.occurred_at.isoformat(),
    )
