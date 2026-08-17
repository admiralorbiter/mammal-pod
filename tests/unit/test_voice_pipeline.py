"""Unit tests for voice trial pipeline, raw media preservation, and non-destructive corrections."""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore
from mammal.capture.voice_pipeline import (
    process_voice_trial_response,
    record_transcription_correction,
)
from mammal.config import Settings
from mammal.events.engine import verify_event_chain
from mammal.models.entities import Artifact, Episode, Experiment, Participant, Protocol, Trial, TrialEvent
from mammal.processors.asr import ASRAdapter, ASRResult, MockASRAdapter


class FailingASRAdapter(ASRAdapter):
    """Adapter that intentionally fails to test pipeline resiliency."""

    def transcribe(self, audio_bytes: bytes, mime_type: str = "audio/webm") -> ASRResult:
        raise RuntimeError("ASR engine failure: out of memory or corrupted audio buffer")


@pytest.fixture
def voice_trial_setup(session: Session):
    participant = Participant(id="part_voice_01", pseudonym="Jonathan (Voice Test)")
    experiment = Experiment(id="e01_voice", title="Semantic Voice Protocol", research_question="Voice question")
    protocol = Protocol(
        protocol_id="e01_semantic_self",
        version="0.1.0",
        domain="semantic",
        mode="observation",
        schema_json={"answer": {"modality": "speech"}},
    )
    session.add_all([participant, experiment, protocol])
    session.flush()

    episode = Episode(
        id="ses_voice_001",
        participant_id=participant.id,
        experiment_id=experiment.id,
        protocol_id=protocol.protocol_id,
        protocol_version=protocol.version,
        mode="observation",
    )
    session.add(episode)
    session.flush()

    trial = Trial(
        id="trl_voice_001",
        episode_id=episode.id,
        item_id="item_geo_001",
        item_version="1.0.0",
        trial_index=1,
    )
    session.add(trial)
    session.commit()
    return {"trial": trial, "episode": episode}


def test_process_voice_trial_response_success(
    session: Session,
    voice_trial_setup,
    temp_settings: Settings,
):
    trial = voice_trial_setup["trial"]
    audio_bytes = b"RIFF....WAVEfmt ... binary audio bytes sample"
    adapter = MockASRAdapter(default_text="Paris", confidence=0.97)

    result = process_voice_trial_response(
        session=session,
        trial_id=trial.id,
        audio_bytes=audio_bytes,
        mime_type="audio/webm",
        asr_adapter=adapter,
        app_settings=temp_settings,
        duration_ms=1450,
    )

    assert result["status"] == "transcribed"
    assert result["text"] == "Paris"
    assert result["raw_artifact_id"] is not None
    assert result["transcript_artifact_id"] is not None

    # Verify raw audio artifact
    raw_art = session.get(Artifact, result["raw_artifact_id"])
    assert raw_art is not None
    assert raw_art.retention_class == "raw"
    assert raw_art.byte_count == len(audio_bytes)

    # Verify derived transcript artifact
    trans_art = session.get(Artifact, result["transcript_artifact_id"])
    assert trans_art is not None
    assert trans_art.retention_class == "derived"
    assert trans_art.source_artifact_ids_json == [raw_art.artifact_id]

    # Verify event chain
    events = (
        session.query(TrialEvent)
        .filter(TrialEvent.trial_id == trial.id)
        .order_by(TrialEvent.occurred_at.asc())
        .all()
    )
    assert len(events) == 2
    assert events[0].event_type == "answer.capture_ended"
    assert events[1].event_type == "transcription.created"
    assert verify_event_chain(events) is True


def test_non_destructive_transcription_correction(
    session: Session,
    voice_trial_setup,
    temp_settings: Settings,
):
    trial = voice_trial_setup["trial"]
    audio_bytes = b"RIFF....audio sample"
    adapter = MockASRAdapter(default_text="Parris", confidence=0.75)

    # 1. Initial transcription
    result = process_voice_trial_response(
        session=session,
        trial_id=trial.id,
        audio_bytes=audio_bytes,
        mime_type="audio/webm",
        asr_adapter=adapter,
        app_settings=temp_settings,
    )
    assert result["text"] == "Parris"

    # 2. Record participant correction
    record_transcription_correction(
        session=session,
        trial_id=trial.id,
        corrected_text="Paris",
        reason="corrected_spelling",
    )

    # 3. Verify that original transcript artifact remains unchanged
    store = ArtifactStore(temp_settings)
    raw_bytes = store.read_artifact_bytes(session, result["raw_artifact_id"])
    assert raw_bytes == audio_bytes

    # 4. Verify correction event is appended to cryptographic chain
    events = (
        session.query(TrialEvent)
        .filter(TrialEvent.trial_id == trial.id)
        .order_by(TrialEvent.occurred_at.asc())
        .all()
    )
    assert len(events) == 3
    assert events[2].event_type == "transcription.corrected"
    assert events[2].payload_json["corrected_text"] == "Paris"
    assert verify_event_chain(events) is True


def test_voice_pipeline_resilient_to_asr_failure(
    session: Session,
    voice_trial_setup,
    temp_settings: Settings,
):
    trial = voice_trial_setup["trial"]
    audio_bytes = b"RIFF....valid audio payload"
    failing_adapter = FailingASRAdapter()

    # Process with failing ASR
    result = process_voice_trial_response(
        session=session,
        trial_id=trial.id,
        audio_bytes=audio_bytes,
        mime_type="audio/webm",
        asr_adapter=failing_adapter,
        app_settings=temp_settings,
    )

    assert result["status"] == "failed"
    assert "ASR engine failure" in result["error"]

    # Crucial exit gate requirement: Raw audio must be saved even if ASR fails!
    raw_art = session.get(Artifact, result["raw_artifact_id"])
    assert raw_art is not None
    assert raw_art.retention_class == "raw"
    assert raw_art.byte_count == len(audio_bytes)

    # Verify transcription.failed event logged
    events = (
        session.query(TrialEvent)
        .filter(TrialEvent.trial_id == trial.id)
        .order_by(TrialEvent.occurred_at.asc())
        .all()
    )
    assert len(events) == 2
    assert events[0].event_type == "answer.capture_ended"
    assert events[1].event_type == "transcription.failed"
    assert verify_event_chain(events) is True
