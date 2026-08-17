"""Integration tests for confidence hardening and answer-only control sessions."""

from __future__ import annotations

import pytest
from flask import Flask
from flask.testing import FlaskClient

from mammal.app import create_app
from mammal.config import Settings
from mammal.db import get_session
from mammal.events.engine import verify_event_chain
from mammal.models.entities import Episode, Trial, TrialEvent


@pytest.fixture
def app(temp_settings: Settings) -> Flask:
    app = create_app(app_settings=temp_settings)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def test_answer_only_control_session_web_flow(client: FlaskClient, temp_settings: Settings):
    # 1. Start answer-only session
    res_start = client.post(
        "/sessions/start",
        data={"protocol_id": "e00_control_answer_only", "pseudonym": "Control User"},
        follow_redirects=False,
    )
    assert res_start.status_code == 302
    episode_id = res_start.headers["Location"].split("/sessions/")[1]

    # 2. Navigate to first trial
    res_session = client.get(f"/sessions/{episode_id}", follow_redirects=False)
    assert res_session.status_code == 302
    trial_url = res_session.headers["Location"]
    trial_id = trial_url.split("/trials/")[1]

    res_trial = client.get(trial_url)
    assert res_trial.status_code == 200
    # Verify confidence section is not displayed in answer-only protocol
    assert b"2. Rate Your Confidence" not in res_trial.data

    # 3. Lock answer (should directly complete trial)
    res_ans = client.post(
        f"/api/trials/{trial_id}/answer",
        json={"value": "Paris", "modality": "button", "latency_ms": 1100},
    )
    assert res_ans.status_code == 200
    ans_data = res_ans.get_json()
    assert ans_data["status"] == "locked"
    assert ans_data["trial_status"] == "completed"

    # 4. Verify trial is completed in database and no confidence was elicited
    with get_session(temp_settings) as session:
        trial = session.get(Trial, trial_id)
        assert trial.status == "completed"
        assert trial.confidence is None
        assert trial.outcome is not None
        assert trial.outcome.is_correct is True

        events = (
            session.query(TrialEvent)
            .filter(TrialEvent.trial_id == trial_id)
            .order_by(TrialEvent.occurred_at.asc())
            .all()
        )
        assert verify_event_chain(events) is True


def test_confidence_elicitation_event_sequence(client: FlaskClient, temp_settings: Settings):
    # 1. Start standard observation session
    res_start = client.post(
        "/sessions/start",
        data={"protocol_id": "e00_instrument_qualification", "pseudonym": "Standard User"},
        follow_redirects=False,
    )
    assert res_start.status_code == 302
    episode_id = res_start.headers["Location"].split("/sessions/")[1]

    res_session = client.get(f"/sessions/{episode_id}", follow_redirects=False)
    trial_id = res_session.headers["Location"].split("/trials/")[1]

    # 2. View trial (triggers prompt shown)
    client.get(f"/sessions/{episode_id}/trials/{trial_id}")

    # 3. Lock answer (triggers confidence.prompt_shown event)
    client.post(
        f"/api/trials/{trial_id}/answer",
        json={"value": "Paris", "modality": "button", "latency_ms": 950},
    )

    # 4. Lock confidence
    client.post(
        f"/api/trials/{trial_id}/confidence",
        json={"value": 75.0, "modality": "numeric", "latency_ms": 1200},
    )

    # 5. Verify event sequence
    with get_session(temp_settings) as session:
        events = (
            session.query(TrialEvent)
            .filter(TrialEvent.trial_id == trial_id)
            .order_by(TrialEvent.occurred_at.asc())
            .all()
        )
        types = [e.event_type for e in events]
        expected_order = [
            "trial.created",
            "prompt.shown",
            "answer.locked",
            "confidence.prompt_shown",
            "confidence.locked",
            "outcome.scored",
            "trial.completed",
        ]
        assert types == expected_order
        assert verify_event_chain(events) is True
