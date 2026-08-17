"""Unit tests for scientific and database state invariants."""

from __future__ import annotations

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from mammal.events.engine import EventEngine, InvariantViolationError
from mammal.models.entities import Answer, Confidence, Episode, Experiment, Outcome, Participant, Protocol, Trial


@pytest.fixture
def test_setup(session: Session):
    """Setup base entities."""
    participant = Participant(id="part_001", pseudonym="Jonathan")
    experiment = Experiment(id="e00", title="Qualification", research_question="Qualification")
    protocol = Protocol(
        protocol_id="proto_001",
        version="1.0.0",
        domain="semantic",
        mode="observation",
        schema_json={},
    )
    session.add_all([participant, experiment, protocol])
    session.flush()

    episode = Episode(
        id="ses_100",
        participant_id=participant.id,
        experiment_id=experiment.id,
        protocol_id=protocol.protocol_id,
        protocol_version=protocol.version,
        mode="observation",
    )
    session.add(episode)
    session.flush()

    trial = Trial(
        id="trl_100",
        episode_id=episode.id,
        item_id="item_001",
        item_version="1.0.0",
        trial_index=1,
    )
    session.add(trial)
    session.commit()
    return {"trial": trial, "episode": episode}


def test_confidence_cannot_precede_answer_lock(session: Session, test_setup):
    trial = test_setup["trial"]
    engine = EventEngine(session)

    # Attempting confidence.locked without answer.locked must fail
    with pytest.raises(InvariantViolationError, match="confidence.locked cannot precede answer.locked"):
        engine.record_event(
            event_type="confidence.locked",
            actor="participant",
            payload={"value": 85.0, "modality": "numeric"},
            trial_id=trial.id,
        )


def test_cannot_modify_locked_answer(session: Session, test_setup):
    trial = test_setup["trial"]
    engine = EventEngine(session)

    engine.record_event(
        event_type="answer.locked",
        actor="participant",
        payload={"modality": "speech", "value": "Answer 1"},
        trial_id=trial.id,
    )

    # Second answer lock on the same trial must fail
    with pytest.raises(InvariantViolationError, match="already has a locked answer"):
        engine.record_event(
            event_type="answer.locked",
            actor="participant",
            payload={"modality": "speech", "value": "Answer 2"},
            trial_id=trial.id,
        )


def test_foreign_key_enforcement(session: Session):
    # Inserting a trial with a non-existent episode must violate foreign keys
    invalid_trial = Trial(
        id="trl_orphan",
        episode_id="non_existent_episode",
        item_id="item_001",
        item_version="1.0.0",
        trial_index=99,
    )
    session.add(invalid_trial)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_confidence_range_constraint(session: Session, test_setup):
    trial = test_setup["trial"]
    # Attempting confidence value > 100 must violate check constraint
    invalid_conf = Confidence(
        trial_id=trial.id,
        value=150.0,
        modality="numeric",
        scale_min=0.0,
        scale_max=100.0,
    )
    session.add(invalid_conf)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
