"""Observer execution engine, prediction persistence, and paired comparison harness."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from sqlalchemy.orm import Session

from mammal.analysis.manifest import create_frozen_target_manifest
from mammal.analysis.paired import PairedComparisonResult, compute_paired_comparison
from mammal.artifacts.store import ArtifactStore
from mammal.config import Settings
from mammal.events.engine import EventEngine
from mammal.observers.acoustic_observer import AcousticProsodyObserver
from mammal.observers.base import ObserverAdapter, ObserverPrediction
from mammal.observers.baselines import (
    DeterministicSolverObserver,
    ItemBaseRateObserver,
    TextConfidenceHeuristicObserver,
    UniformChanceObserver,
)
from mammal.observers.contracts import compile_observer_input

AVAILABLE_OBSERVERS: dict[str, type[ObserverAdapter]] = {
    "uniform_chance": UniformChanceObserver,
    "item_base_rate": ItemBaseRateObserver,
    "deterministic_solver": DeterministicSolverObserver,
    "text_confidence_heuristic": TextConfidenceHeuristicObserver,
    "acoustic_prosody": AcousticProsodyObserver,
}


def get_observer(name: str) -> ObserverAdapter:
    """Instantiate an observer adapter by registered identifier."""
    if name == "personalized_prequential":
        from mammal.personalization.models import PersonalizedPrequentialObserver
        return PersonalizedPrequentialObserver()

    if name not in AVAILABLE_OBSERVERS:
        valid = ", ".join(list(AVAILABLE_OBSERVERS.keys()) + ["personalized_prequential"])
        raise ValueError(f"Unknown observer '{name}'. Available: {valid}")
    return AVAILABLE_OBSERVERS[name]()


def run_observer_on_episode(
    session: Session,
    episode_id: str,
    observer: ObserverAdapter,
    app_settings: Settings | None = None,
) -> dict[str, Any]:
    """Run an observer on a frozen target manifest and compute paired evaluation metrics."""
    # 1. Ensure target manifest exists
    manifest_res = create_frozen_target_manifest(session, episode_id, app_settings=app_settings)
    manifest = manifest_res["manifest"]

    predictions: list[ObserverPrediction] = []
    self_confidences: list[float] = []
    observer_confidences: list[float] = []
    outcomes: list[bool] = []

    event_engine = EventEngine(session)

    # 2. Iterate through trials with strict visibility contract compilation
    for record in manifest.trials:
        compiled_input = compile_observer_input(record, observer.visibility_level)

        # Inject prequential history for personalized observers without future leakage
        if observer.observer_id == "personalized_prequential":
            from mammal.personalization.history import compile_prequential_history
            history = compile_prequential_history(session, manifest.participant_id, record.trial_id)
            compiled_input["prequential_history"] = history
            compiled_input["human_response_latency_ms"] = record.human_response_latency_ms

        pred = observer.predict(compiled_input)
        predictions.append(pred)

        # Telemetry arrays for paired comparison
        if record.human_confidence is not None:
            self_confidences.append(record.human_confidence)
            observer_confidences.append(pred.confidence)
            outcomes.append(record.human_is_correct)

        # Log observer prediction event
        event_engine.record_event(
            trial_id=record.trial_id,
            episode_id=episode_id,
            event_type="observer.prediction_locked",
            actor=f"observer:{observer.observer_id}",
            payload={
                "observer_id": observer.observer_id,
                "version": observer.version,
                "visibility_level": observer.visibility_level.value,
                "predicted_answer": pred.predicted_answer,
                "predicted_probability_correct": pred.predicted_probability_correct,
                "confidence": pred.confidence,
                "latency_ms": pred.latency_ms,
            },
        )

    # 3. Compute paired analysis if trials have confidences
    paired_result: PairedComparisonResult | None = None
    if self_confidences:
        paired_result = compute_paired_comparison(
            episode_id=episode_id,
            observer_id=observer.observer_id,
            self_confidences=self_confidences,
            observer_confidences=observer_confidences,
            outcomes=outcomes,
        )

    # 4. Save observer run artifact
    run_payload = {
        "episode_id": episode_id,
        "observer_id": observer.observer_id,
        "observer_version": observer.version,
        "visibility_level": observer.visibility_level.value,
        "total_trials": len(predictions),
        "predictions": [asdict(p) for p in predictions],
        "paired_comparison": asdict(paired_result) if paired_result else None,
    }

    store = ArtifactStore(app_settings)
    artifact = store.save_derived_artifact(
        session=session,
        content=json.dumps(run_payload, indent=2).encode("utf-8"),
        mime_type="application/json",
        category="derived/observer_runs",
        filename=f"{episode_id}_{observer.observer_id}_run.json",
        source_artifact_ids=[manifest_res["artifact"].artifact_id],
        processor_version=f"{observer.observer_id}-{observer.version}",
    )

    session.commit()

    return {
        "predictions": predictions,
        "paired_result": paired_result,
        "artifact": artifact,
    }
