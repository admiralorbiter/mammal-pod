"""Integration tests for spoken session web workflow, audio uploads, and microphone qualification."""

from __future__ import annotations

import io
import pytest
from flask import Flask
from flask.testing import FlaskClient

from mammal.app import create_app
from mammal.artifacts.store import ArtifactStore
from mammal.config import Settings
from mammal.db import get_session
from mammal.events.engine import verify_event_chain
from mammal.models.entities import Answer, Artifact, Confidence, Episode, Item, Outcome, Trial, TrialEvent


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


def test_microphone_qualification_endpoint(client: FlaskClient):
    res = client.get("/qualification/microphone")
    assert res.status_code == 200
    assert b"Microphone &amp; Speech Input Qualification" in res.data
    assert b"Audio Level Monitor" in res.data


def test_full_spoken_voice_web_session(client: FlaskClient, temp_settings: Settings):
    # 1. Start voice session with e01_semantic_self protocol
    res_start = client.post(
        "/sessions/start",
        data={"protocol_id": "e01_semantic_self", "pseudonym": "Jonathan Lane"},
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
    assert b"Spoken Answer (Voice-First)" in res_trial.data

    # 3. Simulate audio upload from MediaRecorder
    fake_webm_audio = b"G===WEBM_BINARY_AUDIO_HEADER_AND_SAMPLE_SPEECH_DATA===G"
    data = {
        "audio": (io.BytesIO(fake_webm_audio), "response.webm", "audio/webm"),
        "duration_ms": "1650",
    }
    res_upload = client.post(
        f"/api/trials/{trial_id}/audio/upload",
        data=data,
        content_type="multipart/form-data",
    )
    assert res_upload.status_code == 200
    upload_json = res_upload.get_json()
    assert upload_json["status"] == "transcribed"
    raw_art_id = upload_json["raw_artifact_id"]
    transcript_art_id = upload_json["transcript_artifact_id"]
    transcribed_text = upload_json["text"]

    # 4. Determine trial ground truth and record participant transcription correction
    with get_session(temp_settings) as db_sess:
        t_obj = db_sess.get(Trial, trial_id)
        item_obj = db_sess.query(Item).filter(Item.item_id == t_obj.item_id, Item.version == t_obj.item_version).first()
        gt_obj = item_obj.ground_truth_json if item_obj else {}
        expected_ans = gt_obj.get("canonical", "Paris") if isinstance(gt_obj, dict) else str(gt_obj)

    res_correct = client.post(
        f"/api/trials/{trial_id}/transcription/correct",
        json={"corrected_text": expected_ans, "reason": "participant_confirmed"},
    )
    assert res_correct.status_code == 200
    assert res_correct.get_json()["status"] == "corrected"

    # 5. Lock spoken answer
    res_ans = client.post(
        f"/api/trials/{trial_id}/answer",
        json={
            "value": expected_ans,
            "modality": "speech",
            "latency_ms": 2100,
            "raw_artifact_id": raw_art_id,
        },
    )
    assert res_ans.status_code == 200
    assert res_ans.get_json()["status"] == "locked"

    # 6. Lock confidence rating
    res_conf = client.post(
        f"/api/trials/{trial_id}/confidence",
        json={"value": 92.0, "modality": "numeric", "latency_ms": 950},
    )
    assert res_conf.status_code == 200
    assert res_conf.get_json()["status"] == "completed"

    # 7. Verify artifacts and cryptographic event chain in DB
    with get_session(temp_settings) as db_sess:
        store = ArtifactStore(temp_settings)

        # Raw audio integrity check
        assert store.verify_artifact(db_sess, raw_art_id) is True
        raw_art = db_sess.get(Artifact, raw_art_id)
        assert raw_art.retention_class == "raw"

        # Derived transcript check
        assert store.verify_artifact(db_sess, transcript_art_id) is True
        trans_art = db_sess.get(Artifact, transcript_art_id)
        assert trans_art.retention_class == "derived"
        assert trans_art.source_artifact_ids_json == [raw_art_id]

        # Trial answer and outcome checks
        trial = db_sess.get(Trial, trial_id)
        assert trial.status == "completed"
        assert trial.answer.modality == "speech"
        assert trial.answer.locked_value_json == expected_ans
        assert trial.answer.raw_artifact_id == raw_art_id
        assert trial.outcome.is_correct is True
        assert trial.confidence.value == 92.0

        # Verify cryptographic chain
        events = (
            db_sess.query(TrialEvent)
            .filter(TrialEvent.trial_id == trial_id)
            .order_by(TrialEvent.occurred_at.asc())
            .all()
        )
        assert len(events) >= 6
        assert verify_event_chain(events) is True
