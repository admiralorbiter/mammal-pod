"""Integration tests for acoustic extraction pipeline and audio leakage gain analysis."""

from __future__ import annotations

import io
import wave
import numpy as np
from click.testing import CliRunner
from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore
from mammal.cli import main
from mammal.config import Settings
from mammal.models.entities import Artifact, Trial, TrialEvent
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController


def _make_pcm_audio(freq_hz: float = 200.0, duration_sec: float = 0.5) -> bytes:
    sr = 16000
    t = np.linspace(0, duration_sec, int(sr * duration_sec), endpoint=False)
    samples = (0.5 * np.sin(2.0 * np.pi * freq_hz * t) * 32767).astype(np.int16)
    bio = io.BytesIO()
    with wave.open(bio, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(samples.tobytes())
    return bio.getvalue()


def test_full_acoustic_pipeline_and_audio_gain(temp_settings: Settings, session: Session):
    load_and_register_all_protocols(session)

    controller = SessionController(session)
    participant = controller.get_or_create_participant("Acoustic Subject")
    episode = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=4,
    )
    episode_id = episode.id

    store = ArtifactStore(temp_settings)
    trials = session.query(Trial).filter(Trial.episode_id == episode_id).all()

    # 1. Execute trials and save raw audio artifacts
    for i, trial in enumerate(trials):
        item = controller.get_trial_item(trial)
        gt = item.ground_truth_json or {}
        correct_canonical = gt.get("canonical", "Paris")

        # Save synthetic audio artifact
        audio_bytes = _make_pcm_audio(freq_hz=150.0 + i * 20.0)
        audio_art = store.save_raw_artifact(
            session=session,
            content=audio_bytes,
            category="raw/audio",
            filename=f"{trial.id}_speech.wav",
            mime_type="audio/wav",
        )

        controller.mark_prompt_shown(trial.id)
        is_correct = (i < 3)
        ans_val = correct_canonical if is_correct else "Wrong Answer"
        conf_val = 85.0 if is_correct else 35.0

        controller.lock_answer(
            trial.id,
            value=ans_val,
            modality="speech",
            latency_ms=650 + i * 200,
            raw_artifact_id=audio_art.artifact_id,
        )
        controller.lock_confidence(trial.id, value=conf_val, modality="numeric", latency_ms=400)

    session.commit()

    runner = CliRunner()

    # 2. Test CLI extract-acoustics
    res_extract = runner.invoke(
        main,
        ["extract-acoustics", episode_id],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_extract.exit_code == 0
    assert "MAMMAL Acoustic Feature Extraction" in res_extract.output
    assert "Successfully extracted acoustic features for 4 spoken trials" in res_extract.output

    # 3. Verify acoustic.extracted events in DB
    events = session.query(TrialEvent).filter(TrialEvent.episode_id == episode_id).all()
    acoustics_events = [e for e in events if e.event_type == "acoustic.extracted"]
    assert len(acoustics_events) == 4

    # 4. Test CLI audio-gain
    res_gain = runner.invoke(
        main,
        ["audio-gain", episode_id],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_gain.exit_code == 0
    assert "MAMMAL Public Signal & Audio Leakage Gain" in res_gain.output
    assert "Acoustic Prosody Channel" in res_gain.output
