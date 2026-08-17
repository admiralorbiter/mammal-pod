"""Deterministic trial state reconstruction from event streams."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Sequence

from mammal.events.engine import InvariantViolationError, verify_event_chain
from mammal.models.entities import TrialEvent


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
