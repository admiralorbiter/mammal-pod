"""Unit tests for feedback policy enforcement and observation silence."""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from mammal.events.engine import verify_event_chain
from mammal.items.bank import seed_qualification_items
from mammal.models.entities import Protocol, TrialEvent
from mammal.protocols.loader import load_protocol_file, register_protocol
from mammal.trials.controller import SessionController


def test_observation_mode_feedback_silence(session: Session):
    # Load observation protocol e00_instrument_qualification
    proto_data = load_protocol_file("config/e00_instrument_qualification.yaml")
    register_protocol(session, proto_data)
    seed_qualification_items(session)
    session.commit()

    controller = SessionController(session)
    participant = controller.get_or_create_participant("Silent Participant")
    episode = controller.start_session("e00_instrument_qualification", participant.id, item_limit=1)

    trial = controller.get_active_trial(episode.id)
    controller.lock_answer(trial.id, value="Paris", modality="button")
    controller.lock_confidence(trial.id, value=85.0, modality="numeric")

    # Verify event stream has NO feedback.shown event
    events = (
        session.query(TrialEvent)
        .filter(TrialEvent.trial_id == trial.id)
        .order_by(TrialEvent.occurred_at.asc())
        .all()
    )
    event_types = [e.event_type for e in events]
    assert "feedback.shown" not in event_types
    assert verify_event_chain(events) is True


def test_trial_level_feedback_event_emission(session: Session):
    # Construct a protocol with trial-level feedback enabled (e.g. calibration intervention)
    feedback_proto_data = {
        "protocol_id": "e08_calibration_feedback_test",
        "version": "0.1.0",
        "status": "engineering",
        "domain": "semantic",
        "mode": "intervention",
        "prompt_modality": "visual",
        "answer": {"modality": "button", "lock_required": True},
        "confidence": {"enabled": True, "minimum": 0, "maximum": 100, "shown_after_answer_lock": True},
        "feedback": {"trial_level": True, "block_level": False, "show_model_predictions": False},
        "item_bank": {"bank_id": "synthetic_e00", "version": "0.1.0", "partition": "engineering"},
        "analysis": {"primary_estimands": ["calibration_change"], "analysis_plan": "docs/04_EXPERIMENT_PROGRAM_AND_GATES.md#e08"},
    }
    register_protocol(session, feedback_proto_data)
    seed_qualification_items(session)
    session.commit()

    controller = SessionController(session)
    participant = controller.get_or_create_participant("Feedback Participant")
    episode = controller.start_session("e08_calibration_feedback_test", participant.id, item_limit=1)

    trial = controller.get_active_trial(episode.id)
    controller.lock_answer(trial.id, value="Paris", modality="button")
    controller.lock_confidence(trial.id, value=90.0, modality="numeric")

    # Verify event stream DOES contain feedback.shown event
    events = (
        session.query(TrialEvent)
        .filter(TrialEvent.trial_id == trial.id)
        .order_by(TrialEvent.occurred_at.asc())
        .all()
    )
    event_types = [e.event_type for e in events]
    assert "feedback.shown" in event_types

    fb_event = next(e for e in events if e.event_type == "feedback.shown")
    assert fb_event.payload_json["is_correct"] is True
    assert verify_event_chain(events) is True
