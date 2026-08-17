"""Integration test verifying full synthetic trial lifecycle and deterministic event replay."""

from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore
from mammal.events.engine import EventEngine
from mammal.models.entities import (
    Answer,
    Confidence,
    Episode,
    Experiment,
    Item,
    Outcome,
    Participant,
    Protocol,
    Trial,
)
from mammal.trials.replay import replay_trial_events


def test_full_synthetic_trial_and_deterministic_replay(
    session: Session,
    artifact_store: ArtifactStore,
):
    # 1. Setup scientific context
    participant = Participant(id="part_jonathan_01", pseudonym="Jonathan Lane")
    experiment = Experiment(
        id="e00_inst_qualification",
        title="Instrument Qualification",
        research_question="Can the system preserve a complete, immutable, replayable trial record?",
        status="engineering",
    )
    protocol = Protocol(
        protocol_id="proto_semantic_speech_v1",
        version="1.0.0",
        domain="semantic",
        mode="observation",
        schema_json={"answer_modality": "speech", "confidence": {"scale": "0-100"}},
    )
    item = Item(
        item_id="item_capitals_france",
        version="1.0.0",
        domain="semantic",
        family="geography_capitals",
        prompt_json={"question": "What is the capital of France?"},
        options_json=["Lyon", "Marseille", "Paris", "Toulouse"],
        ground_truth_json={"canonical": "Paris"},
        partition="engineering",
        source_json={"provenance": "synthetic_qualification_fixture"},
        content_hash="mock_item_hash_001",
    )
    session.add_all([participant, experiment, protocol, item])
    session.flush()

    episode = Episode(
        id="ses_synth_001",
        participant_id=participant.id,
        experiment_id=experiment.id,
        protocol_id=protocol.protocol_id,
        protocol_version=protocol.version,
        mode="engineering",
        started_at=datetime.now(timezone.utc),
    )
    session.add(episode)
    session.flush()

    trial = Trial(
        id="trl_synth_001",
        episode_id=episode.id,
        item_id=item.item_id,
        item_version=item.version,
        trial_index=1,
        condition="spoken_answer",
    )
    session.add(trial)
    session.flush()

    # 2. Artifact capture (raw audio)
    raw_audio_bytes = b"RIFF....WAVEfmt ... synthetic speech audio saying Paris"
    audio_art = artifact_store.save_raw_artifact(
        session=session,
        content=raw_audio_bytes,
        mime_type="audio/webm",
        category="raw/audio",
        filename=f"{trial.id}_response.webm",
    )
    session.flush()

    # 3. Append-only event sequence
    engine = EventEngine(session)

    engine.record_event(
        event_type="trial.created",
        actor="server",
        payload={"item_id": item.item_id, "trial_index": 1},
        trial_id=trial.id,
        episode_id=episode.id,
    )
    engine.record_event(
        event_type="prompt.shown",
        actor="browser",
        payload={"prompt_id": item.item_id, "render_latency_ms": 12.5},
        trial_id=trial.id,
        episode_id=episode.id,
    )
    engine.record_event(
        event_type="answer.capture_started",
        actor="browser",
        payload={"modality": "speech"},
        trial_id=trial.id,
        episode_id=episode.id,
    )
    engine.record_event(
        event_type="answer.capture_ended",
        actor="browser",
        payload={"duration_ms": 1420},
        trial_id=trial.id,
        episode_id=episode.id,
    )
    engine.record_event(
        event_type="answer.locked",
        actor="participant",
        payload={
            "modality": "speech",
            "value": "Paris",
            "raw_artifact_id": audio_art.artifact_id,
            "latency_ms": 1850.0,
        },
        trial_id=trial.id,
        episode_id=episode.id,
    )

    # Derived transcript artifact
    transcript_bytes = b'{"transcript": "Paris", "confidence": 0.99}'
    transcript_art = artifact_store.save_derived_artifact(
        session=session,
        content=transcript_bytes,
        mime_type="application/json",
        category="derived/transcripts",
        filename=f"{trial.id}_transcript.json",
        source_artifact_ids=[audio_art.artifact_id],
        processor_version="faster-whisper-mock-1.0",
    )
    session.flush()

    engine.record_event(
        event_type="transcription.created",
        actor="processor",
        payload={
            "artifact_id": transcript_art.artifact_id,
            "text": "Paris",
            "asr_confidence": 0.99,
        },
        trial_id=trial.id,
        episode_id=episode.id,
    )

    engine.record_event(
        event_type="confidence.prompt_shown",
        actor="browser",
        payload={"scale": "0-100"},
        trial_id=trial.id,
        episode_id=episode.id,
    )
    engine.record_event(
        event_type="confidence.locked",
        actor="participant",
        payload={"value": 95.0, "modality": "numeric", "latency_ms": 940.0},
        trial_id=trial.id,
        episode_id=episode.id,
    )

    engine.record_event(
        event_type="outcome.scored",
        actor="processor",
        payload={
            "is_correct": True,
            "score": 1.0,
            "scoring_rule": "exact_match",
            "scorer": "ground_truth_validator",
        },
        trial_id=trial.id,
        episode_id=episode.id,
    )
    engine.record_event(
        event_type="trial.completed",
        actor="server",
        payload={"status": "success"},
        trial_id=trial.id,
        episode_id=episode.id,
    )

    session.commit()

    # 4. Replay and verify state reconstruction
    events = engine.get_trial_events(trial.id)
    assert len(events) == 10

    replayed = replay_trial_events(events)

    assert replayed.trial_id == trial.id
    assert replayed.status == "completed"
    assert replayed.answer is not None
    assert replayed.answer.modality == "speech"
    assert replayed.answer.locked_value == "Paris"
    assert replayed.answer.raw_artifact_id == audio_art.artifact_id
    assert replayed.answer.response_latency_ms == 1850.0

    assert replayed.confidence is not None
    assert replayed.confidence.value == 95.0
    assert replayed.confidence.latency_ms == 940.0

    assert replayed.outcome is not None
    assert replayed.outcome.is_correct is True
    assert replayed.outcome.score == 1.0
    assert replayed.outcome.scoring_rule == "exact_match"

    assert len(replayed.transcripts) == 1
    assert replayed.transcripts[0]["text"] == "Paris"

    assert audio_art.artifact_id in replayed.artifacts
    assert transcript_art.artifact_id in replayed.artifacts

    # 5. Audit all artifacts
    audit = artifact_store.verify_all_artifacts(session)
    assert audit["status"] == "PASS"
    assert audit["verified"] == 2
    assert len(audit["corrupted"]) == 0
    assert len(audit["missing"]) == 0
