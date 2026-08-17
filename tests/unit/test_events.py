"""Unit tests for append-only event engine and cryptographic chaining."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy.orm import Session

from mammal.events.engine import (
    EventEngine,
    InvariantViolationError,
    canonical_json_dumps,
    compute_event_hash,
    verify_event_chain,
)
from mammal.models.entities import Episode, Experiment, Participant, Protocol, Trial, TrialEvent


@pytest.fixture
def test_setup(session: Session):
    """Setup base entities needed for trial events."""
    participant = Participant(id="part_test_01", pseudonym="Jonathan (Pilot)")
    experiment = Experiment(
        id="e00_inst_qual",
        title="Instrument Qualification",
        research_question="Can the system preserve a complete trial record?",
    )
    protocol = Protocol(
        protocol_id="e00_qual",
        version="1.0.0",
        domain="semantic",
        mode="engineering",
        schema_json={"test": True},
    )
    session.add_all([participant, experiment, protocol])
    session.flush()

    episode = Episode(
        id="ses_001",
        participant_id=participant.id,
        experiment_id=experiment.id,
        protocol_id=protocol.protocol_id,
        protocol_version=protocol.version,
        mode="engineering",
    )
    session.add(episode)
    session.flush()

    trial = Trial(
        id="trl_001",
        episode_id=episode.id,
        item_id="item_geo_001",
        item_version="1.0.0",
        trial_index=1,
    )
    session.add(trial)
    session.commit()
    return {"participant": participant, "episode": episode, "trial": trial}


def test_canonical_json_dumps():
    obj1 = {"b": 2, "a": 1, "nested": {"z": 10, "y": 20}}
    obj2 = {"nested": {"y": 20, "z": 10}, "a": 1, "b": 2}
    assert canonical_json_dumps(obj1) == canonical_json_dumps(obj2)
    assert canonical_json_dumps(obj1) == '{"a":1,"b":2,"nested":{"y":20,"z":10}}'


def test_event_chaining(session: Session, test_setup):
    trial = test_setup["trial"]
    engine = EventEngine(session)

    e1 = engine.record_event(
        event_type="trial.created",
        actor="server",
        payload={"item_id": trial.item_id},
        trial_id=trial.id,
    )
    assert e1.previous_event_hash is None
    assert e1.event_hash is not None

    e2 = engine.record_event(
        event_type="prompt.shown",
        actor="browser",
        payload={"rendered_at_ms": 12345},
        trial_id=trial.id,
    )
    assert e2.previous_event_hash == e1.event_hash

    e3 = engine.record_event(
        event_type="answer.locked",
        actor="participant",
        payload={"modality": "speech", "value": "Paris"},
        trial_id=trial.id,
    )
    assert e3.previous_event_hash == e2.event_hash

    events = engine.get_trial_events(trial.id)
    assert len(events) == 3
    assert verify_event_chain(events) is True


def test_verify_event_chain_detects_tampering(session: Session, test_setup):
    trial = test_setup["trial"]
    engine = EventEngine(session)

    engine.record_event(
        event_type="trial.created",
        actor="server",
        payload={"item_id": trial.item_id},
        trial_id=trial.id,
    )
    engine.record_event(
        event_type="prompt.shown",
        actor="browser",
        payload={"latency": 50},
        trial_id=trial.id,
    )
    session.commit()

    events = engine.get_trial_events(trial.id)

    # Tamper with the in-memory payload of event 0
    events[0].payload_json = {"item_id": "MODIFIED_ITEM_ID"}

    with pytest.raises(InvariantViolationError, match="Tampering detected"):
        verify_event_chain(events)
