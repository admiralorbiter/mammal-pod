"""Memory session analysis engine evaluating prospective Judgments of Learning against future recall."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any
from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore
from mammal.config import Settings
from mammal.models.entities import TrialEvent
from mammal.memory.metrics import compute_prospective_memory_metrics


@dataclass
class MemoryEpisodeAnalysis:
    """Prospective memory resolution analysis for a study-recall episode."""

    episode_id: str
    total_pairs: int
    recall_accuracy: float
    mean_jol: float
    gamma_correlation: float
    prospective_auroc: float
    prospective_brier_score: float
    pair_details: list[dict[str, Any]]


def analyze_memory_episode(
    session: Session,
    episode_id: str,
    app_settings: Settings | None = None,
) -> dict[str, Any]:
    """Extract encoding JOL forecasts and paired recall outcomes to compute prospective resolution."""
    events = (
        session.query(TrialEvent)
        .filter(TrialEvent.episode_id == episode_id)
        .order_by(TrialEvent.occurred_at.asc())
        .all()
    )

    # 1. Map JOLs by item_id or cue
    jols: dict[str, dict[str, Any]] = {}
    for e in events:
        if e.event_type == "memory.jol_locked":
            item_id = e.payload_json.get("item_id") or e.trial_id
            jols[item_id] = {
                "encoding_trial_id": e.trial_id,
                "cue": e.payload_json.get("cue", ""),
                "jol_rating": float(e.payload_json.get("jol_rating", 50.0)),
                "jol_latency_ms": float(e.payload_json.get("jol_latency_ms", 0.0)),
            }

    # 2. Map recall outcomes
    recalls: dict[str, dict[str, Any]] = {}
    for e in events:
        if e.event_type == "memory.recall_scored":
            item_id = e.payload_json.get("item_id") or e.payload_json.get("encoding_trial_id") or e.trial_id
            recalls[item_id] = {
                "recall_trial_id": e.trial_id,
                "target": e.payload_json.get("target", ""),
                "is_correct": bool(e.payload_json.get("is_correct", False)),
                "score": float(e.payload_json.get("score", 0.0)),
            }

    # 3. Align pairs
    matched_jols: list[float] = []
    matched_outcomes: list[bool] = []
    pair_details: list[dict[str, Any]] = []

    for item_id, j_data in jols.items():
        if item_id in recalls:
            r_data = recalls[item_id]
            matched_jols.append(j_data["jol_rating"])
            matched_outcomes.append(r_data["is_correct"])

            pair_details.append({
                "item_id": item_id,
                "cue": j_data["cue"],
                "target": r_data["target"],
                "jol_rating": j_data["jol_rating"],
                "is_correct": r_data["is_correct"],
            })

    if not matched_outcomes:
        raise ValueError(f"No matched encoding-recall pairs found in episode {episode_id}")

    # 4. Compute prospective metrics
    metrics = compute_prospective_memory_metrics(matched_jols, matched_outcomes)

    analysis = MemoryEpisodeAnalysis(
        episode_id=episode_id,
        total_pairs=len(matched_outcomes),
        recall_accuracy=metrics["recall_accuracy"],
        mean_jol=metrics["mean_jol"],
        gamma_correlation=metrics["gamma_correlation"],
        prospective_auroc=metrics["prospective_auroc"],
        prospective_brier_score=metrics["prospective_brier_score"],
        pair_details=pair_details,
    )

    # 5. Save derived artifact
    store = ArtifactStore(app_settings)
    payload_bytes = json.dumps(asdict(analysis), indent=2).encode("utf-8")
    artifact = store.save_derived_artifact(
        session=session,
        content=payload_bytes,
        mime_type="application/json",
        category="derived/memory",
        filename=f"{episode_id}_memory_analysis.json",
        source_artifact_ids=[],
        processor_version="memory-kernel-v1.0",
    )

    session.commit()

    return {
        "analysis": analysis,
        "artifact": artifact,
    }
