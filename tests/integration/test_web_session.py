"""Integration tests for manual session web flow, server-side locking, and observation silence."""

from __future__ import annotations

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from mammal.app import create_app
from mammal.config import Settings
from mammal.db import get_session
from mammal.events.engine import verify_event_chain
from mammal.models.entities import Answer, Confidence, Episode, Outcome, Trial, TrialEvent


@pytest.fixture
def app(temp_settings: Settings) -> Flask:
    """Create Flask test application configured with temporary data root."""
    app = create_app(app_settings=temp_settings)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Provide Flask test client."""
    return app.test_client()


def test_full_web_manual_session_and_observation_silence(client: FlaskClient, temp_settings: Settings):
    # 1. Access dashboard
    res_index = client.get("/")
    assert res_index.status_code == 200
    assert b"Metacognitive Assessment" in res_index.data

    # 2. Start session
    res_start = client.post(
        "/sessions/start",
        data={"protocol_id": "e00_instrument_qualification", "pseudonym": "Jonathan Lane"},
        follow_redirects=False,
    )
    assert res_start.status_code == 302
    redirect_url = res_start.headers["Location"]
    episode_id = redirect_url.split("/sessions/")[1]

    # 3. Follow session routing to first trial
    res_session = client.get(f"/sessions/{episode_id}", follow_redirects=False)
    assert res_session.status_code == 302
    trial_url = res_session.headers["Location"]
    trial_id = trial_url.split("/trials/")[1]

    # 4. View first trial
    res_trial_view = client.get(trial_url)
    assert res_trial_view.status_code == 200
    assert b"TRIAL 1 OF" in res_trial_view.data

    # 5. Invariant check: attempting confidence before answer lock must fail (400)
    res_conf_early = client.post(
        f"/api/trials/{trial_id}/confidence",
        json={"value": 75.0, "modality": "numeric"},
    )
    assert res_conf_early.status_code == 400
    assert "Cannot lock confidence before answer" in res_conf_early.get_json()["error"]

    # 6. Lock answer
    res_answer = client.post(
        f"/api/trials/{trial_id}/answer",
        json={"value": "Paris", "modality": "button", "latency_ms": 1200},
    )
    assert res_answer.status_code == 200
    assert res_answer.get_json()["status"] == "locked"

    # 7. Invariant check: cannot modify locked answer (400)
    res_answer_dup = client.post(
        f"/api/trials/{trial_id}/answer",
        json={"value": "Lyon", "modality": "button"},
    )
    assert res_answer_dup.status_code == 400
    assert "already has a locked answer" in res_answer_dup.get_json()["error"]

    # 8. Lock confidence
    res_conf = client.post(
        f"/api/trials/{trial_id}/confidence",
        json={"value": 90.0, "modality": "numeric", "latency_ms": 800},
    )
    assert res_conf.status_code == 200
    assert res_conf.get_json()["status"] == "completed"

    # 9. Play through remaining trials in episode
    while True:
        res_next = client.get(f"/sessions/{episode_id}", follow_redirects=False)
        if "/summary" in res_next.headers["Location"]:
            break
        curr_trial_id = res_next.headers["Location"].split("/trials/")[1]

        # Load trial
        client.get(f"/sessions/{episode_id}/trials/{curr_trial_id}")

        # Submit answer & confidence
        client.post(
            f"/api/trials/{curr_trial_id}/answer",
            json={"value": "Test Answer", "modality": "button"},
        )
        client.post(
            f"/api/trials/{curr_trial_id}/confidence",
            json={"value": 50.0, "modality": "numeric"},
        )

    # 10. View session summary and verify observation silence
    res_summary = client.get(f"/sessions/{episode_id}/summary")
    assert res_summary.status_code == 200
    html_text = res_summary.data.decode("utf-8")

    assert "Session Recorded Successfully" in html_text
    assert "SILENCE ACTIVE" in html_text

    # Verify no trial-level correctness feedback is exposed
    assert "Correct Answer:" not in html_text
    assert "Your Score:" not in html_text
    assert "Accuracy:" not in html_text

    # 11. Verify database integrity and cryptographic event chains
    with get_session(temp_settings) as db_sess:
        episode = db_sess.get(Episode, episode_id)
        assert episode.status == "completed"
        assert episode.ended_at is not None

        trials = db_sess.query(Trial).filter(Trial.episode_id == episode_id).all()
        assert len(trials) > 0

        for trl in trials:
            assert trl.status == "completed"
            assert trl.answer is not None
            assert trl.confidence is not None
            assert trl.outcome is not None

            # Verify cryptographic event chain
            events = (
                db_sess.query(TrialEvent)
                .filter(TrialEvent.trial_id == trl.id)
                .order_by(TrialEvent.occurred_at.asc())
                .all()
            )
            assert len(events) >= 5
            assert verify_event_chain(events) is True
