"""Unit tests for cryptographically frozen target manifests."""

from __future__ import annotations

import json
from sqlalchemy.orm import Session

from mammal.analysis.manifest import create_frozen_target_manifest
from mammal.artifacts.store import ArtifactStore
from mammal.config import Settings
from mammal.models.entities import Trial, TrialEvent
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController


def test_create_frozen_target_manifest(session: Session, temp_settings: Settings):
    load_and_register_all_protocols(session)
    controller = SessionController(session)
    participant = controller.get_or_create_participant("Manifest Benchmark User")

    episode = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=6,
    )
    episode_id = episode.id

    trials = session.query(Trial).filter(Trial.episode_id == episode_id).all()
    assert len(trials) == 6

    # Execute and score all 6 trials
    for i, trial in enumerate(trials):
        item = controller.get_trial_item(trial)
        gt = item.ground_truth_json or {}
        correct_canonical = gt.get("canonical", "Paris")

        controller.mark_prompt_shown(trial.id)
        is_correct = (i % 2 == 0)
        ans_val = correct_canonical if is_correct else "Wrong Answer"
        conf_val = 85.0 if is_correct else 35.0

        controller.lock_answer(trial.id, value=ans_val, modality="button", latency_ms=500)
        controller.lock_confidence(trial.id, value=conf_val, modality="numeric", latency_ms=300)

    session.commit()

    # Create target manifest
    result = create_frozen_target_manifest(session, episode_id, app_settings=temp_settings)
    manifest = result["manifest"]
    artifact = result["artifact"]

    # Verify manifest integrity
    assert manifest.episode_id == episode_id
    assert manifest.total_trials == 6
    assert len(manifest.manifest_hash) == 64
    assert len(manifest.trials) == 6

    # Verify trial record details
    first_record = manifest.trials[0]
    assert first_record.human_is_correct is True
    assert first_record.human_confidence == 85.0
    assert first_record.human_response_latency_ms == 500.0

    second_record = manifest.trials[1]
    assert second_record.human_is_correct is False
    assert second_record.human_confidence == 35.0

    # Verify artifact in store
    store = ArtifactStore(temp_settings)
    content_bytes = store.read_artifact_bytes(session, artifact.artifact_id)
    parsed = json.loads(content_bytes.decode("utf-8"))
    assert parsed["manifest_hash"] == manifest.manifest_hash

    # Verify manifest.frozen event in event stream
    events = session.query(TrialEvent).filter(TrialEvent.episode_id == episode_id).all()
    event_types = [e.event_type for e in events]
    assert "manifest.frozen" in event_types
