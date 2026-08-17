"""Memory study encoding phase and Judgment of Learning (JOL) forecast lock."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from sqlalchemy.orm import Session

from mammal.events.engine import EventEngine


@dataclass
class MemoryStudyItem:
    """Associative cue-target pair for memory study encoding."""

    item_id: str
    cue: str
    target: str
    category: str = "paired_associates"


@dataclass
class EncodingTrialRecord:
    """Recorded encoding trial with frozen prospective Judgment of Learning (JOL)."""

    trial_id: str
    episode_id: str
    item_id: str
    cue: str
    target: str
    study_duration_ms: float
    jol_rating: float  # In [0.0, 100.0]
    jol_latency_ms: float


def record_encoding_jol(
    session: Session,
    trial_id: str,
    episode_id: str,
    item_id: str,
    cue: str,
    target: str,
    study_duration_ms: float,
    jol_rating: float,
    jol_latency_ms: float,
) -> EncodingTrialRecord:
    """Immutably freeze prospective Judgment of Learning forecast in the event stream."""
    if not (0.0 <= jol_rating <= 100.0):
        raise ValueError(f"JOL rating must be in range [0.0, 100.0], got {jol_rating}")

    event_engine = EventEngine(session)

    # 1. Log study presentation event
    event_engine.record_event(
        trial_id=trial_id,
        episode_id=episode_id,
        event_type="memory.study_presented",
        actor="system:experimenter",
        payload={
            "item_id": item_id,
            "cue": cue,
            "target": target,
            "study_duration_ms": study_duration_ms,
        },
    )

    # 2. Immutably freeze JOL forecast before retention interval
    event_engine.record_event(
        trial_id=trial_id,
        episode_id=episode_id,
        event_type="memory.jol_locked",
        actor="participant:human",
        payload={
            "item_id": item_id,
            "cue": cue,
            "jol_rating": jol_rating,
            "jol_latency_ms": jol_latency_ms,
        },
    )

    session.commit()

    return EncodingTrialRecord(
        trial_id=trial_id,
        episode_id=episode_id,
        item_id=item_id,
        cue=cue,
        target=target,
        study_duration_ms=study_duration_ms,
        jol_rating=jol_rating,
        jol_latency_ms=jol_latency_ms,
    )
