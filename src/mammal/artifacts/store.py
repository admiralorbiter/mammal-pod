"""Artifact storage, SHA-256 integrity verification, and lineage tracking."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from mammal.config import Settings, settings
from mammal.models.entities import Artifact


def compute_sha256(data: bytes) -> str:
    """Compute deterministic SHA-256 hex digest of byte string."""
    return hashlib.sha256(data).hexdigest()


class ArtifactStore:
    """Manages file storage, checksums, and artifact records."""

    def __init__(self, app_settings: Settings | None = None) -> None:
        self.settings = app_settings or settings
        self.settings.ensure_directories()

    def _resolve_path(self, rel_path: str) -> Path:
        """Resolve relative path against data root."""
        return self.settings.data_root / rel_path

    def save_raw_artifact(
        self,
        session: Session,
        content: bytes,
        mime_type: str,
        category: str,
        filename: str,
        artifact_id: str | None = None,
    ) -> Artifact:
        """Save an immutable raw artifact to disk and register in database."""
        sha256 = compute_sha256(content)
        rel_path = f"{category.strip('/')}/{filename}"
        full_path = self._resolve_path(rel_path)
        full_path.parent.mkdir(parents=True, exist_ok=True)

        full_path.write_bytes(content)

        artifact = Artifact(
            artifact_id=artifact_id or f"art_raw_{sha256[:16]}",
            sha256=sha256,
            mime_type=mime_type,
            rel_path=rel_path,
            byte_count=len(content),
            source_artifact_ids_json=None,
            processor_version=None,
            retention_class="raw",
        )
        session.add(artifact)
        return artifact

    def save_derived_artifact(
        self,
        session: Session,
        content: bytes,
        mime_type: str,
        category: str,
        filename: str,
        source_artifact_ids: Sequence[str],
        processor_version: str,
        artifact_id: str | None = None,
    ) -> Artifact:
        """Save a derived artifact linked to its parent source artifacts."""
        sha256 = compute_sha256(content)
        rel_path = f"{category.strip('/')}/{filename}"
        full_path = self._resolve_path(rel_path)
        full_path.parent.mkdir(parents=True, exist_ok=True)

        full_path.write_bytes(content)

        artifact = Artifact(
            artifact_id=artifact_id or f"art_drv_{sha256[:16]}",
            sha256=sha256,
            mime_type=mime_type,
            rel_path=rel_path,
            byte_count=len(content),
            source_artifact_ids_json=list(source_artifact_ids),
            processor_version=processor_version,
            retention_class="derived",
        )
        session.add(artifact)
        return artifact

    def read_artifact_bytes(self, session: Session, artifact_id: str) -> bytes:
        """Read artifact content bytes after verifying checksum."""
        artifact = session.get(Artifact, artifact_id)
        if not artifact:
            raise FileNotFoundError(f"Artifact {artifact_id} not registered in database.")

        full_path = self._resolve_path(artifact.rel_path)
        if not full_path.exists():
            raise FileNotFoundError(f"Artifact file missing on disk: {full_path}")

        content = full_path.read_bytes()
        actual_sha = compute_sha256(content)
        if actual_sha != artifact.sha256:
            raise ValueError(
                f"Artifact corruption detected for {artifact_id}! "
                f"Expected {artifact.sha256}, got {actual_sha}"
            )
        return content

    def verify_artifact(self, session: Session, artifact_id: str) -> bool:
        """Verify checksum of an individual artifact on disk."""
        self.read_artifact_bytes(session, artifact_id)
        return True

    def verify_all_artifacts(self, session: Session) -> dict[str, Any]:
        """Audit all registered artifacts against on-disk files."""
        artifacts = session.scalars(select(Artifact)).all()
        verified = 0
        corrupted = []
        missing = []

        for art in artifacts:
            full_path = self._resolve_path(art.rel_path)
            if not full_path.exists():
                missing.append(art.artifact_id)
                continue

            content = full_path.read_bytes()
            if compute_sha256(content) != art.sha256:
                corrupted.append(art.artifact_id)
            else:
                verified += 1

        return {
            "total": len(artifacts),
            "verified": verified,
            "corrupted": corrupted,
            "missing": missing,
            "status": "PASS" if not corrupted and not missing else "FAIL",
        }
