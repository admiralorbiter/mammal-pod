"""Unit tests for cold session backup export, archive restoration, and post-restore replay."""

from __future__ import annotations

from pathlib import Path
import pytest
from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore
from mammal.backup.archive import export_session_archive, restore_session_archive
from mammal.capture.voice_pipeline import process_voice_trial_response
from mammal.config import Settings
from mammal.db import get_session
from mammal.models.entities import Episode
from mammal.processors.asr import MockASRAdapter
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController
from mammal.trials.replay import replay_session_from_events


def test_export_and_restore_session_cycle(tmp_path: Path, temp_settings: Settings, session: Session):
    # 1. Setup session in source environment
    load_and_register_all_protocols(session)
    controller = SessionController(session)
    participant = controller.get_or_create_participant("Export Test User")
    episode = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=2,
    )
    episode_id = episode.id

    # 2. Complete trial 1 with voice recording & transcript
    trial1 = controller.get_active_trial(episode_id)
    voice_res = process_voice_trial_response(
        session=session,
        trial_id=trial1.id,
        audio_bytes=b"RIFF....SAMPLE_VOICE_PAYLOAD",
        mime_type="audio/webm",
        asr_adapter=MockASRAdapter(default_text="Paris", confidence=0.98),
        app_settings=temp_settings,
    )
    controller.lock_answer(trial1.id, value="Paris", modality="speech", raw_artifact_id=voice_res["raw_artifact_id"])
    controller.lock_confidence(trial1.id, value=95.0, modality="numeric")

    # 3. Complete trial 2 with manual button
    trial2 = controller.get_active_trial(episode_id)
    controller.lock_answer(trial2.id, value="Nile", modality="button")
    controller.lock_confidence(trial2.id, value=80.0, modality="numeric")

    session.commit()

    # 4. Export archive to temporary tarball
    archive_path = tmp_path / f"{episode_id}_archive.tar.gz"
    out_tar = export_session_archive(
        session=session,
        episode_id=episode_id,
        output_path=archive_path,
        app_settings=temp_settings,
    )
    assert out_tar.exists()
    assert out_tar.stat().st_size > 0

    # 5. Create fresh clean destination data root
    dest_settings = Settings.load(custom_data_root=tmp_path / "restored_mammal_data")
    dest_settings.ensure_directories()

    # 6. Restore archive into fresh destination
    restored_ep_id = restore_session_archive(
        archive_path=out_tar,
        target_settings=dest_settings,
    )
    assert restored_ep_id == episode_id

    # 7. Execute deterministic replay and SHA-256 audit on restored environment
    with get_session(dest_settings) as dest_session:
        summary = replay_session_from_events(
            session=dest_session,
            episode_id=restored_ep_id,
            app_settings=dest_settings,
        )

        assert summary.is_valid is True
        assert summary.total_trials == 2
        assert summary.replayed_trials == 2
        assert summary.total_artifacts_verified >= 2
        assert len(summary.discrepancies) == 0
