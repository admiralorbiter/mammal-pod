"""Cued recall testing phase, fuzzy scoring, and missing response handling."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any
from sqlalchemy.orm import Session

from mammal.events.engine import EventEngine


@dataclass
class RecallTrialRecord:
    """Recorded cued recall trial outcome matched against encoding JOL."""

    recall_trial_id: str
    encoding_trial_id: str
    episode_id: str
    item_id: str
    cue: str
    target: str
    provided_answer: str
    is_correct: bool
    score: float
    response_latency_ms: float


def _normalize_string(text: str) -> str:
    """Normalize text by trimming, lowercasing, and stripping punctuation."""
    t = text.strip().lower()
    t = re.sub(r"[^\w\s]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def score_cued_recall(
    provided_answer: str,
    target_answer: str,
    acceptable_alternatives: list[str] | None = None,
) -> tuple[bool, float]:
    """Score a participant's cued recall attempt with robust string normalization."""
    if not provided_answer or provided_answer.strip().lower() in {"missing", "timeout", "pass", "idk", "don't know"}:
        return False, 0.0

    norm_provided = _normalize_string(provided_answer)
    norm_target = _normalize_string(target_answer)

    if norm_provided == norm_target:
        return True, 1.0

    if acceptable_alternatives:
        for alt in acceptable_alternatives:
            if norm_provided == _normalize_string(alt):
                return True, 1.0

    return False, 0.0


def record_cued_recall(
    session: Session,
    recall_trial_id: str,
    encoding_trial_id: str,
    episode_id: str,
    item_id: str,
    cue: str,
    target: str,
    provided_answer: str,
    response_latency_ms: float,
    acceptable_alternatives: list[str] | None = None,
) -> RecallTrialRecord:
    """Record and score a cued recall attempt linked to its prior encoding trial."""
    is_corr, score = score_cued_recall(provided_answer, target, acceptable_alternatives)

    event_engine = EventEngine(session)

    # 1. Log recall answered event
    event_engine.record_event(
        trial_id=recall_trial_id,
        episode_id=episode_id,
        event_type="memory.recall_answered",
        actor="participant:human",
        payload={
            "encoding_trial_id": encoding_trial_id,
            "item_id": item_id,
            "cue": cue,
            "provided_answer": provided_answer,
            "response_latency_ms": response_latency_ms,
        },
    )

    # 2. Log recall scored event
    event_engine.record_event(
        trial_id=recall_trial_id,
        episode_id=episode_id,
        event_type="memory.recall_scored",
        actor="scorer:exact_normalized",
        payload={
            "encoding_trial_id": encoding_trial_id,
            "item_id": item_id,
            "target": target,
            "is_correct": is_corr,
            "score": score,
        },
    )

    session.commit()

    return RecallTrialRecord(
        recall_trial_id=recall_trial_id,
        encoding_trial_id=encoding_trial_id,
        episode_id=episode_id,
        item_id=item_id,
        cue=cue,
        target=target,
        provided_answer=provided_answer,
        is_correct=is_corr,
        score=score,
        response_latency_ms=response_latency_ms,
    )
