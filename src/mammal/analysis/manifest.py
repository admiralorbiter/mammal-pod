"""Frozen target manifests for Human Self baselines and observer evaluation datasets."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore, compute_sha256
from mammal.config import Settings
from mammal.events.engine import EventEngine, canonical_json_dumps
from mammal.models.entities import Episode, Item, Trial


@dataclass
class TargetTrialRecord:
    """Immutable trial performance record of the human participant."""

    trial_id: str
    trial_index: int
    item_id: str
    item_version: str
    item_content_hash: str
    domain: str
    prompt_payload: dict[str, Any]
    options: list[str] | None
    ground_truth: dict[str, Any]
    human_locked_answer: Any
    human_confidence: float | None
    human_is_correct: bool
    human_score: float
    human_response_latency_ms: float | None
    human_confidence_latency_ms: float | None


@dataclass
class FrozenTargetManifest:
    """Cryptographically frozen target manifest for observer prediction benchmarks."""

    episode_id: str
    participant_id: str
    protocol_id: str
    protocol_version: str
    total_trials: int
    manifest_hash: str
    frozen_at: str
    trials: list[TargetTrialRecord] = field(default_factory=list)


def create_frozen_target_manifest(
    session: Session,
    episode_id: str,
    app_settings: Settings | None = None,
) -> dict[str, Any]:
    """Freeze a completed human session into an immutable target dataset for generic/personalized observers."""
    episode = session.get(Episode, episode_id)
    if not episode:
        raise ValueError(f"Episode {episode_id} not found.")

    trials = (
        session.query(Trial)
        .filter(Trial.episode_id == episode_id)
        .order_by(Trial.trial_index.asc())
        .all()
    )
    if not trials:
        raise ValueError(f"Episode {episode_id} contains no trials.")

    trial_records: list[TargetTrialRecord] = []

    for trial in trials:
        if trial.outcome is None or trial.answer is None:
            continue

        item = session.query(Item).filter(Item.item_id == trial.item_id, Item.version == trial.item_version).first()
        item_hash = item.content_hash if item else ""
        item_domain = item.domain if item else "unknown"
        options = item.options_json if item else None
        ground_truth = item.ground_truth_json if item else {}
        prompt_payload = item.prompt_json if item else {}

        record = TargetTrialRecord(
            trial_id=trial.id,
            trial_index=trial.trial_index,
            item_id=trial.item_id,
            item_version=trial.item_version,
            item_content_hash=item_hash,
            domain=item_domain,
            prompt_payload=prompt_payload,
            options=options,
            ground_truth=ground_truth,
            human_locked_answer=trial.answer.locked_value_json,
            human_confidence=trial.confidence.value if trial.confidence else None,
            human_is_correct=trial.outcome.is_correct,
            human_score=trial.outcome.score,
            human_response_latency_ms=trial.answer.response_latency_ms,
            human_confidence_latency_ms=trial.confidence.latency_ms if trial.confidence else None,
        )
        trial_records.append(record)

    if not trial_records:
        raise ValueError(f"Episode {episode_id} has no completed and scored trials.")

    # Compute deterministic cryptographic manifest hash over canonical JSON of trials
    canonical_trials_json = canonical_json_dumps([asdict(r) for r in trial_records])
    manifest_hash = compute_sha256(canonical_trials_json.encode("utf-8"))
    frozen_at = datetime.utcnow().isoformat() + "Z"

    manifest = FrozenTargetManifest(
        episode_id=episode_id,
        participant_id=episode.participant_id or "unknown",
        protocol_id=episode.protocol_id,
        protocol_version=episode.protocol_version,
        total_trials=len(trial_records),
        manifest_hash=manifest_hash,
        frozen_at=frozen_at,
        trials=trial_records,
    )

    # Save derived artifact in ArtifactStore
    store = ArtifactStore(app_settings)
    manifest_bytes = json.dumps(asdict(manifest), indent=2).encode("utf-8")
    artifact = store.save_derived_artifact(
        session=session,
        content=manifest_bytes,
        mime_type="application/json",
        category="derived/manifests",
        filename=f"{episode_id}_target_manifest.json",
        source_artifact_ids=[],
        processor_version="target-manifest-v1.0",
    )

    # Append manifest.frozen event
    event_engine = EventEngine(session)
    event_engine.record_event(
        episode_id=episode_id,
        event_type="manifest.frozen",
        actor="processor",
        payload={
            "artifact_id": artifact.artifact_id,
            "manifest_hash": manifest_hash,
            "total_trials": len(trial_records),
        },
    )

    session.commit()

    return {
        "manifest": manifest,
        "artifact": artifact,
    }
