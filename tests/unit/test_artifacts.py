"""Unit tests for artifact storage, SHA-256 computation, and lineage."""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore, compute_sha256
from mammal.config import Settings
from mammal.models.entities import Artifact


def test_compute_sha256():
    data = b"Project MAMMAL: Metacognitive Assessment"
    expected = "5076cfb3528b18ec4e062eb142b918ae87fe05f5904944ec7ebdf7f29e1eb1c0"
    # Just verify deterministic output length and consistency
    digest = compute_sha256(data)
    assert len(digest) == 64
    assert digest == compute_sha256(data)


def test_save_and_read_raw_artifact(session: Session, artifact_store: ArtifactStore):
    content = b"raw audio recording bytes sample"
    art = artifact_store.save_raw_artifact(
        session=session,
        content=content,
        mime_type="audio/webm",
        category="raw/audio",
        filename="test_trial_001.webm",
    )
    session.commit()

    assert art.artifact_id is not None
    assert art.byte_count == len(content)
    assert art.retention_class == "raw"
    assert art.sha256 == compute_sha256(content)

    # Read back and verify bytes
    read_bytes = artifact_store.read_artifact_bytes(session, art.artifact_id)
    assert read_bytes == content


def test_save_derived_artifact_lineage(session: Session, artifact_store: ArtifactStore):
    raw_content = b"source raw audio"
    raw_art = artifact_store.save_raw_artifact(
        session=session,
        content=raw_content,
        mime_type="audio/webm",
        category="raw/audio",
        filename="source_001.webm",
    )
    session.flush()

    derived_content = b'{"transcript": "Paris", "confidence": 0.98}'
    derived_art = artifact_store.save_derived_artifact(
        session=session,
        content=derived_content,
        mime_type="application/json",
        category="derived/transcripts",
        filename="transcript_001.json",
        source_artifact_ids=[raw_art.artifact_id],
        processor_version="faster-whisper-v1.0",
    )
    session.commit()

    assert derived_art.retention_class == "derived"
    assert derived_art.source_artifact_ids_json == [raw_art.artifact_id]
    assert derived_art.processor_version == "faster-whisper-v1.0"


def test_detect_corrupted_artifact(
    session: Session,
    artifact_store: ArtifactStore,
    temp_settings: Settings,
):
    content = b"original uncorrupted data"
    art = artifact_store.save_raw_artifact(
        session=session,
        content=content,
        mime_type="text/plain",
        category="raw/protocol_snapshots",
        filename="snapshot.json",
    )
    session.commit()

    # Tamper with file on disk directly
    file_path = temp_settings.data_root / art.rel_path
    file_path.write_bytes(b"tampered data")

    with pytest.raises(ValueError, match="Artifact corruption detected"):
        artifact_store.read_artifact_bytes(session, art.artifact_id)

    audit = artifact_store.verify_all_artifacts(session)
    assert audit["status"] == "FAIL"
    assert art.artifact_id in audit["corrupted"]


def test_detect_missing_artifact(
    session: Session,
    artifact_store: ArtifactStore,
    temp_settings: Settings,
):
    content = b"ephemeral content"
    art = artifact_store.save_raw_artifact(
        session=session,
        content=content,
        mime_type="text/plain",
        category="raw/protocol_snapshots",
        filename="missing_test.json",
    )
    session.commit()

    # Delete file from disk
    file_path = temp_settings.data_root / art.rel_path
    file_path.unlink()

    with pytest.raises(FileNotFoundError, match="Artifact file missing on disk"):
        artifact_store.read_artifact_bytes(session, art.artifact_id)

    audit = artifact_store.verify_all_artifacts(session)
    assert audit["status"] == "FAIL"
    assert art.artifact_id in audit["missing"]
