"""Audio capture ingestion and raw artifact storage."""

from __future__ import annotations

from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore
from mammal.config import Settings
from mammal.models.entities import Artifact


def resolve_audio_extension(mime_type: str) -> str:
    """Map audio MIME type to file extension."""
    clean_mime = mime_type.split(";")[0].strip().lower()
    mapping = {
        "audio/webm": ".webm",
        "audio/wav": ".wav",
        "audio/x-wav": ".wav",
        "audio/mp3": ".mp3",
        "audio/mpeg": ".mp3",
        "audio/ogg": ".ogg",
        "audio/flac": ".flac",
    }
    return mapping.get(clean_mime, ".webm")


def save_trial_audio_upload(
    session: Session,
    trial_id: str,
    audio_bytes: bytes,
    mime_type: str = "audio/webm",
    app_settings: Settings | None = None,
) -> Artifact:
    """Save an immutable raw audio recording for a trial."""
    if not audio_bytes or len(audio_bytes) < 4:
        raise ValueError("Cannot save empty or invalid audio capture.")

    store = ArtifactStore(app_settings)
    ext = resolve_audio_extension(mime_type)
    filename = f"{trial_id}_response{ext}"

    artifact = store.save_raw_artifact(
        session=session,
        content=audio_bytes,
        mime_type=mime_type,
        category="raw/audio",
        filename=filename,
        artifact_id=f"art_raw_audio_{trial_id}",
    )
    return artifact
