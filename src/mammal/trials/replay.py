"""Deterministic trial and session state reconstruction from cryptographic event streams."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Sequence

from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore
from mammal.config import Settings
from mammal.events.engine import InvariantViolationError, verify_event_chain
from mammal.models.entities import Episode, Trial, TrialEvent


@dataclass
class ReplayedAnswerState:
    modality: str
    locked_value: Any
    locked_at: datetime
    raw_artifact_id: str | None = None
    response_latency_ms: float | None = None


@dataclass
class ReplayedConfidenceState:
    value: float
    modality: str
    locked_at: datetime
    raw_artifact_id: str | None = None
    latency_ms: float | None = None


@dataclass
class ReplayedOutcomeState:
    is_correct: bool
    score: float
    scoring_rule: str
    scorer: str
    scored_at: datetime


@dataclass
class ReplayedTrialState:
    trial_id: str
    status: str = "created"
    prompt_shown_at: datetime | None = None
    answer: ReplayedAnswerState | None = None
    confidence: ReplayedConfidenceState | None = None
    outcome: ReplayedOutcomeState | None = None
    transcripts: list[dict[str, Any]] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    event_count: int = 0


@dataclass
class SessionReplaySummary:
    """Audit summary of session deterministic event replay."""

    episode_id: str
    total_trials: int
    replayed_trials: int
    total_events: int
    total_artifacts_verified: int
    is_valid: bool
    discrepancies: list[str] = field(default_factory=list)
    trials: list[ReplayedTrialState] = field(default_factory=list)


def replay_trial_events(events: Sequence[TrialEvent]) -> ReplayedTrialState:
    """Replay an event stream to construct the canonical trial state."""
    if not events:
        raise ValueError("Cannot replay empty event stream.")

    verify_event_chain(events)

    trial_id = events[0].trial_id or "unknown"
    state = ReplayedTrialState(trial_id=trial_id)

    for event in events:
        state.event_count += 1
        etype = event.event_type
        payload = event.payload_json or {}

        if etype == "trial.created":
            state.status = "created"

        elif etype == "prompt.shown":
            state.status = "prompt_shown"
            state.prompt_shown_at = event.occurred_at

        elif etype == "stimulus.started":
            state.status = "stimulus_active"

        elif etype == "stimulus.ended":
            state.status = "stimulus_ended"

        elif etype == "answer.locked":
            if state.answer is not None:
                raise InvariantViolationError(f"Duplicate answer.locked in trial {trial_id}")
            state.answer = ReplayedAnswerState(
                modality=payload.get("modality", "unknown"),
                locked_value=payload.get("value"),
                locked_at=event.occurred_at,
                raw_artifact_id=payload.get("raw_artifact_id"),
                response_latency_ms=payload.get("latency_ms"),
            )
            state.status = "answer_locked"
            if payload.get("raw_artifact_id"):
                state.artifacts.append(payload["raw_artifact_id"])

        elif etype == "confidence.locked":
            if state.answer is None:
                raise InvariantViolationError(f"confidence.locked encountered before answer.locked in {trial_id}")
            state.confidence = ReplayedConfidenceState(
                value=float(payload["value"]),
                modality=payload.get("modality", "numeric"),
                locked_at=event.occurred_at,
                raw_artifact_id=payload.get("raw_artifact_id"),
                latency_ms=payload.get("latency_ms"),
            )
            state.status = "confidence_locked"
            if payload.get("raw_artifact_id"):
                state.artifacts.append(payload["raw_artifact_id"])

        elif etype == "outcome.scored":
            state.outcome = ReplayedOutcomeState(
                is_correct=bool(payload["is_correct"]),
                score=float(payload.get("score", 1.0 if payload["is_correct"] else 0.0)),
                scoring_rule=payload.get("scoring_rule", "exact_match"),
                scorer=payload.get("scorer", "deterministic"),
                scored_at=event.occurred_at,
            )

        elif etype == "transcription.created":
            state.transcripts.append(payload)
            if payload.get("artifact_id"):
                state.artifacts.append(payload["artifact_id"])

        elif etype == "transcription.corrected":
            state.transcripts.append({"correction": payload})

        elif etype == "trial.completed":
            state.status = "completed"

    return state


def replay_session_from_events(
    session: Session,
    episode_id: str,
    app_settings: Settings | None = None,
) -> SessionReplaySummary:
    """Perform deterministic state reconstruction and cryptographic verification for an entire session."""
    episode = session.get(Episode, episode_id)
    if not episode:
        raise ValueError(f"Episode {episode_id} not found in database.")

    trials = (
        session.query(Trial)
        .filter(Trial.episode_id == episode_id)
        .order_by(Trial.trial_index.asc())
        .all()
    )

    store = ArtifactStore(app_settings)
    discrepancies: list[str] = []
    replayed_trials: list[ReplayedTrialState] = []
    total_events = 0
    total_artifacts = 0

    for trial in trials:
        events = (
            session.query(TrialEvent)
            .filter(TrialEvent.trial_id == trial.id)
            .order_by(TrialEvent.occurred_at.asc())
            .all()
        )
        total_events += len(events)

        if not events:
            discrepancies.append(f"Trial {trial.id} has no recorded events.")
            continue

        try:
            replayed = replay_trial_events(events)
            replayed_trials.append(replayed)

            # 1. Verify trial status consistency
            if replayed.status != trial.status:
                discrepancies.append(
                    f"Trial {trial.id} status mismatch: DB='{trial.status}' vs Replayed='{replayed.status}'"
                )

            # 2. Verify answer consistency
            if trial.answer is not None:
                if replayed.answer is None:
                    discrepancies.append(f"Trial {trial.id} missing replayed answer.")
                elif replayed.answer.locked_value != trial.answer.locked_value_json:
                    discrepancies.append(
                        f"Trial {trial.id} answer mismatch: DB='{trial.answer.locked_value_json}' vs Replayed='{replayed.answer.locked_value}'"
                    )

            # 3. Verify confidence consistency
            if trial.confidence is not None:
                if replayed.confidence is None:
                    discrepancies.append(f"Trial {trial.id} missing replayed confidence.")
                elif replayed.confidence.value != trial.confidence.value:
                    discrepancies.append(
                        f"Trial {trial.id} confidence mismatch: DB={trial.confidence.value} vs Replayed={replayed.confidence.value}"
                    )

            # 4. Verify outcome consistency
            if trial.outcome is not None:
                if replayed.outcome is None:
                    discrepancies.append(f"Trial {trial.id} missing replayed outcome.")
                elif replayed.outcome.is_correct != trial.outcome.is_correct:
                    discrepancies.append(
                        f"Trial {trial.id} outcome is_correct mismatch: DB={trial.outcome.is_correct} vs Replayed={replayed.outcome.is_correct}"
                    )

            # 5. Verify associated artifacts on disk
            for art_id in replayed.artifacts:
                try:
                    if store.verify_artifact(session, art_id):
                        total_artifacts += 1
                    else:
                        discrepancies.append(f"Artifact {art_id} failed SHA-256 verification.")
                except Exception as exc:
                    discrepancies.append(f"Artifact {art_id} verification error: {exc}")

        except Exception as exc:
            discrepancies.append(f"Trial {trial.id} replay failed: {exc}")

    is_valid = len(discrepancies) == 0

    return SessionReplaySummary(
        episode_id=episode_id,
        total_trials=len(trials),
        replayed_trials=len(replayed_trials),
        total_events=total_events,
        total_artifacts_verified=total_artifacts,
        is_valid=is_valid,
        discrepancies=discrepancies,
        trials=replayed_trials,
    )
