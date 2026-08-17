"""Append-only event sourcing engine with cryptographic chain integrity."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from mammal.artifacts.store import compute_sha256
from mammal.models.base import generate_uuid, utc_now
from mammal.models.entities import Trial, TrialEvent


class InvariantViolationError(Exception):
    """Raised when an append-only event or state transition violates scientific rules."""


def canonical_json_dumps(obj: Any) -> str:
    """Produce deterministic canonical JSON string."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


from datetime import datetime, timezone


def normalize_datetime_iso(dt: datetime | str) -> str:
    """Normalize datetime to consistent ISO 8601 UTC string."""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.isoformat()


def compute_event_hash(
    previous_event_hash: str | None,
    event_id: str,
    trial_id: str | None,
    episode_id: str | None,
    event_type: str,
    occurred_at: datetime | str,
    actor: str,
    schema_version: str,
    payload: dict[str, Any],
) -> str:
    """Compute deterministic SHA-256 hash of an event."""
    iso_occurred = normalize_datetime_iso(occurred_at)
    canonical_payload = canonical_json_dumps(payload)
    chain_input = (
        f"{previous_event_hash or ''}|{event_id}|{trial_id or ''}|"
        f"{episode_id or ''}|{event_type}|{iso_occurred}|{actor}|"
        f"{schema_version}|{canonical_payload}"
    )
    return compute_sha256(chain_input.encode("utf-8"))


class EventEngine:
    """Handles appending, validating, and querying append-only trial events."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_latest_event(self, trial_id: str | None = None, episode_id: str | None = None) -> TrialEvent | None:
        """Fetch the most recent event for a given trial or episode."""
        stmt = select(TrialEvent)
        if trial_id:
            stmt = stmt.where(TrialEvent.trial_id == trial_id)
        elif episode_id:
            stmt = stmt.where(TrialEvent.episode_id == episode_id)
        stmt = stmt.order_by(TrialEvent.occurred_at.desc(), TrialEvent.recorded_at.desc())
        return self.session.scalars(stmt).first()

    def get_trial_events(self, trial_id: str) -> list[TrialEvent]:
        """Fetch all events for a trial ordered by occurred_at."""
        stmt = (
            select(TrialEvent)
            .where(TrialEvent.trial_id == trial_id)
            .order_by(TrialEvent.occurred_at.asc(), TrialEvent.recorded_at.asc())
        )
        return list(self.session.scalars(stmt).all())

    def validate_invariants(
        self,
        trial_id: str | None,
        event_type: str,
        payload: dict[str, Any],
    ) -> None:
        """Enforce strict scientific lifecycle rules before recording events."""
        if not trial_id:
            return

        existing_events = self.get_trial_events(trial_id)
        existing_types = [e.event_type for e in existing_events]

        # Rule 1: Cannot lock answer twice
        if event_type == "answer.locked" and "answer.locked" in existing_types:
            raise InvariantViolationError(f"Trial {trial_id} already has a locked answer. Answers cannot be modified.")

        # Rule 2: Cannot lock confidence before answer is locked
        if event_type == "confidence.locked":
            if "answer.locked" not in existing_types:
                raise InvariantViolationError(
                    f"Violation for trial {trial_id}: confidence.locked cannot precede answer.locked."
                )
            if "confidence.locked" in existing_types:
                raise InvariantViolationError(
                    f"Trial {trial_id} already has a locked confidence. Confidence cannot be re-locked."
                )

        # Rule 3: Trial completed requires both answer and confidence (unless answer-only protocol mode)
        if event_type == "trial.completed":
            if "answer.locked" not in existing_types:
                raise InvariantViolationError(f"Cannot complete trial {trial_id} without locked answer.")

    def record_event(
        self,
        event_type: str,
        actor: str,
        payload: dict[str, Any],
        trial_id: str | None = None,
        episode_id: str | None = None,
        occurred_at: datetime | None = None,
        schema_version: str = "1.0.0",
        event_id: str | None = None,
    ) -> TrialEvent:
        """Append a validated, cryptographically chained event to the log."""
        self.validate_invariants(trial_id, event_type, payload)

        eid = event_id or f"evt_{generate_uuid()}"
        ts_occurred = occurred_at or utc_now()
        ts_recorded = utc_now()

        # Find latest event in chain
        latest = self.get_latest_event(trial_id=trial_id, episode_id=episode_id if not trial_id else None)
        prev_hash = latest.event_hash if latest else None

        event_hash = compute_event_hash(
            previous_event_hash=prev_hash,
            event_id=eid,
            trial_id=trial_id,
            episode_id=episode_id,
            event_type=event_type,
            occurred_at=ts_occurred,
            actor=actor,
            schema_version=schema_version,
            payload=payload,
        )

        event = TrialEvent(
            event_id=eid,
            trial_id=trial_id,
            episode_id=episode_id,
            event_type=event_type,
            occurred_at=ts_occurred,
            recorded_at=ts_recorded,
            actor=actor,
            schema_version=schema_version,
            payload_json=payload,
            previous_event_hash=prev_hash,
            event_hash=event_hash,
        )
        self.session.add(event)
        self.session.flush()
        return event


def verify_event_chain(events: Sequence[TrialEvent]) -> bool:
    """Verify cryptographic chain continuity and payload integrity of an event sequence."""
    prev_hash: str | None = None
    for idx, event in enumerate(events):
        if event.previous_event_hash != prev_hash:
            raise InvariantViolationError(
                f"Chain link broken at event index {idx} ({event.event_id}): "
                f"expected previous_hash '{prev_hash}', got '{event.previous_event_hash}'"
            )

        expected_hash = compute_event_hash(
            previous_event_hash=prev_hash,
            event_id=event.event_id,
            trial_id=event.trial_id,
            episode_id=event.episode_id,
            event_type=event.event_type,
            occurred_at=event.occurred_at,
            actor=event.actor,
            schema_version=event.schema_version,
            payload=event.payload_json,
        )
        if expected_hash != event.event_hash:
            raise InvariantViolationError(
                f"Tampering detected at event index {idx} ({event.event_id}): "
                f"expected event_hash '{expected_hash}', recorded '{event.event_hash}'"
            )

        prev_hash = event.event_hash
    return True
