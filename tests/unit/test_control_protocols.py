"""Unit tests for answer-only control protocols (confidence disabled)."""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from mammal.items.bank import seed_qualification_items
from mammal.models.entities import Episode, Experiment, Participant, Protocol, Trial, TrialEvent
from mammal.protocols.loader import load_protocol_file, register_protocol
from mammal.trials.controller import SessionController


def test_answer_only_control_protocol_workflow(session: Session):
    # 1. Load and register e00_control_answer_only protocol
    proto_data = load_protocol_file("config/e00_control_answer_only.yaml")
    protocol = register_protocol(session, proto_data)
    seed_qualification_items(session)
    session.commit()

    controller = SessionController(session)
    participant = controller.get_or_create_participant("Control Participant")
    episode = controller.start_session(
        protocol_id="e00_control_answer_only",
        participant_id=participant.id,
        item_limit=2,
    )

    # 2. Get first trial
    trial = controller.get_active_trial(episode.id)
    assert trial is not None
    assert trial.status == "created"

    # 3. Lock answer (should immediately score and complete trial without confidence elicitation)
    answer = controller.lock_answer(
        trial_id=trial.id,
        value="Paris",
        modality="button",
        latency_ms=1250,
    )
    assert answer is not None

    # 4. Check trial status and outcome
    session.refresh(trial)
    assert trial.status == "completed"
    assert trial.answer is not None
    assert trial.confidence is None  # No confidence elicited
    assert trial.outcome is not None
    assert trial.outcome.is_correct is True

    # 5. Check events recorded
    events = (
        session.query(TrialEvent)
        .filter(TrialEvent.trial_id == trial.id)
        .order_by(TrialEvent.occurred_at.asc())
        .all()
    )
    event_types = [e.event_type for e in events]
    assert "answer.locked" in event_types
    assert "outcome.scored" in event_types
    assert "trial.completed" in event_types
    assert "confidence.locked" not in event_types
    assert "confidence.prompt_shown" not in event_types
