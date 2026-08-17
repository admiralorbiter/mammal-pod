"""Voice trial execution pipeline, raw preservation, and transcription correction."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore
from mammal.capture.audio import save_trial_audio_upload
from mammal.config import Settings
from mammal.events.engine import EventEngine
from mammal.models.entities import Trial
from mammal.processors.asr import ASRAdapter, get_asr_adapter


def process_voice_trial_response(
    session: Session,
    trial_id: str,
    audio_bytes: bytes,
    mime_type: str = "audio/webm",
    asr_adapter: ASRAdapter | None = None,
    app_settings: Settings | None = None,
    duration_ms: float | None = None,
) -> dict[str, Any]:
    """Process incoming participant audio: save raw, transcribe, and register derived artifact."""
    trial = session.get(Trial, trial_id)
    if not trial:
        raise ValueError(f"Trial {trial_id} not found.")

    events = EventEngine(session)
    store = ArtifactStore(app_settings)

    # 1. Save raw audio artifact unconditionally before any model processing
    raw_art = save_trial_audio_upload(
        session=session,
        trial_id=trial_id,
        audio_bytes=audio_bytes,
        mime_type=mime_type,
        app_settings=app_settings,
    )
    session.flush()

    # 2. Record capture ended event
    events.record_event(
        event_type="answer.capture_ended",
        actor="browser",
        payload={
            "raw_artifact_id": raw_art.artifact_id,
            "byte_count": raw_art.byte_count,
            "duration_ms": duration_ms,
            "mime_type": mime_type,
        },
        trial_id=trial_id,
        episode_id=trial.episode_id,
    )

    # 3. Transcribe audio with ASR adapter
    adapter = asr_adapter or get_asr_adapter("mock")

    try:
        asr_res = adapter.transcribe(audio_bytes, mime_type=mime_type)

        # 4. Save derived transcript artifact
        transcript_json_bytes = json.dumps(
            {
                "text": asr_res.text,
                "confidence": asr_res.confidence,
                "duration_s": asr_res.duration_s,
                "processor_version": asr_res.processor_version,
                "language": asr_res.language,
                "segments": asr_res.segments,
            },
            sort_keys=True,
            indent=2,
        ).encode("utf-8")

        transcript_art = store.save_derived_artifact(
            session=session,
            content=transcript_json_bytes,
            mime_type="application/json",
            category="derived/transcripts",
            filename=f"{trial_id}_transcript.json",
            source_artifact_ids=[raw_art.artifact_id],
            processor_version=asr_res.processor_version,
            artifact_id=f"art_drv_transcript_{trial_id}",
        )
        session.flush()

        # 5. Record transcription created event
        events.record_event(
            event_type="transcription.created",
            actor="processor",
            payload={
                "artifact_id": transcript_art.artifact_id,
                "text": asr_res.text,
                "asr_confidence": asr_res.confidence,
                "processor_version": asr_res.processor_version,
            },
            trial_id=trial_id,
            episode_id=trial.episode_id,
        )

        session.commit()

        return {
            "status": "transcribed",
            "text": asr_res.text,
            "raw_artifact_id": raw_art.artifact_id,
            "transcript_artifact_id": transcript_art.artifact_id,
            "asr_confidence": asr_res.confidence,
            "processor_version": asr_res.processor_version,
        }

    except Exception as exc:
        # Resilient error mode: raw audio is preserved, record transcription.failed
        events.record_event(
            event_type="transcription.failed",
            actor="processor",
            payload={
                "raw_artifact_id": raw_art.artifact_id,
                "error": str(exc),
            },
            trial_id=trial_id,
            episode_id=trial.episode_id,
        )
        session.commit()

        return {
            "status": "failed",
            "error": str(exc),
            "raw_artifact_id": raw_art.artifact_id,
        }


def record_transcription_correction(
    session: Session,
    trial_id: str,
    corrected_text: str,
    reason: str = "participant_review",
) -> None:
    """Record an append-only transcription correction event without altering raw media."""
    trial = session.get(Trial, trial_id)
    if not trial:
        raise ValueError(f"Trial {trial_id} not found.")

    events = EventEngine(session)
    events.record_event(
        event_type="transcription.corrected",
        actor="participant",
        payload={
            "corrected_text": corrected_text,
            "reason": reason,
        },
        trial_id=trial_id,
        episode_id=trial.episode_id,
    )
    session.commit()
