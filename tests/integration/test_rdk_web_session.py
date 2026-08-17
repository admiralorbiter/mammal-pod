"""Integration tests for visual psychophysics, display qualification, and RDK trial flows."""

from __future__ import annotations

import pytest
from flask import Flask
from flask.testing import FlaskClient

from mammal.app import create_app
from mammal.config import Settings
from mammal.db import get_session
from mammal.models.entities import Episode, Trial, TrialEvent
from mammal.protocols.loader import load_and_register_all_protocols


@pytest.fixture
def app(temp_settings: Settings) -> Flask:
    app = create_app(app_settings=temp_settings)
    app.config["TESTING"] = True
    with get_session(temp_settings) as session:
        load_and_register_all_protocols(session)
        session.commit()
    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def test_display_qualification_web_endpoint(client: FlaskClient):
    # 1. Test GET /qualification/display
    res_get = client.get("/qualification/display")
    assert res_get.status_code == 200
    assert b"DISPLAY QUALIFICATION" in res_get.data

    # 2. Test POST /api/qualification/display with valid 60Hz intervals
    intervals = [16.67] * 120
    res_post = client.post(
        "/api/qualification/display",
        json={
            "frame_intervals_ms": intervals,
            "viewport_width": 1920,
            "viewport_height": 1080,
            "device_pixel_ratio": 1.0,
            "fullscreen": True,
        },
    )
    assert res_post.status_code == 200
    data = res_post.get_json()
    assert data["is_qualified"] is True
    assert data["estimated_refresh_rate_hz"] == pytest.approx(60.0, abs=1.0)


def test_rdk_perceptual_session_flow(client: FlaskClient, temp_settings: Settings):
    # 1. Start RDK session
    res_start = client.post(
        "/sessions/start",
        data={
            "pseudonym": "Perceptual Tester",
            "protocol_id": "p01_rdk_staircase",
        },
        follow_redirects=True,
    )
    assert res_start.status_code == 200
    assert b"RDK MOTION DISCRIMINATION" in res_start.data

    with get_session(temp_settings) as session:
        episode = session.query(Episode).filter(Episode.protocol_id == "p01_rdk_staircase").first()
        assert episode is not None
        trial = session.query(Trial).filter(Trial.episode_id == episode.id).first()
        assert trial is not None
        trial_id = trial.id

    # 2. Trigger stimulus start
    res_stim = client.post(f"/api/trials/{trial_id}/stimulus/start", json={"client_time_ms": 1000.0})
    assert res_stim.status_code == 200

    # 3. Submit answer with frame telemetry
    frame_deltas = [16.66, 16.67, 16.68, 16.65, 16.67] * 12
    res_ans = client.post(
        f"/api/trials/{trial_id}/answer",
        json={
            "value": "left",
            "modality": "button",
            "latency_ms": 720,
            "frame_intervals_ms": frame_deltas,
        },
    )
    assert res_ans.status_code == 200

    # 4. Verify stimulus.started and stimulus.ended events in DB
    with get_session(temp_settings) as session:
        events = (
            session.query(TrialEvent)
            .filter(TrialEvent.trial_id == trial_id)
            .order_by(TrialEvent.occurred_at.asc())
            .all()
        )
        event_types = [e.event_type for e in events]
        assert "stimulus.started" in event_types
        assert "stimulus.ended" in event_types
        assert "answer.locked" in event_types
