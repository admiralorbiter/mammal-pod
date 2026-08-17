"""Statistical analysis engine, artifact report generation, and epistemic summarization."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
import numpy as np

from sqlalchemy.orm import Session

from mammal.analysis.bootstrap import block_bootstrap_ci
from mammal.analysis.metrics import (
    compute_accuracy,
    compute_auroc2,
    compute_brier_score,
    compute_expected_calibration_error,
    compute_type2_sdt,
)
from mammal.artifacts.store import ArtifactStore
from mammal.config import Settings
from mammal.events.engine import EventEngine
from mammal.models.entities import Answer, Artifact, Confidence, Episode, Outcome, Protocol, Trial



@dataclass
class MetricWithCI:
    estimate: float
    ci_lower: float
    ci_upper: float


@dataclass
class AnalysisResult:
    episode_id: str
    protocol_id: str
    protocol_version: str
    mode: str
    n_trials: int
    n_scored: int
    accuracy: MetricWithCI
    brier_score: MetricWithCI
    ece: MetricWithCI
    auroc2: MetricWithCI
    d_prime: float
    meta_d_prime: float
    m_ratio: float
    mean_answer_latency_ms: float | None
    mean_confidence_latency_ms: float | None
    calibration_bins: list[dict[str, Any]]
    analyzed_at: str


def analyze_episode(
    session: Session,
    episode_id: str,
    n_bootstraps: int = 200,
) -> AnalysisResult:
    """Compute prespecified empirical estimands, calibration, and Type-2 SDT metrics for a completed episode."""
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

    trial_data: list[dict[str, Any]] = []
    answer_latencies: list[float] = []
    confidence_latencies: list[float] = []

    for trial in trials:
        if trial.outcome is not None:
            ans = trial.answer
            conf = trial.confidence
            out = trial.outcome

            conf_val = conf.value if conf is not None else 100.0 if out.is_correct else 0.0
            if ans and ans.response_latency_ms is not None:
                answer_latencies.append(ans.response_latency_ms)
            if conf and conf.latency_ms is not None:
                confidence_latencies.append(conf.latency_ms)

            trial_data.append({
                "trial_id": trial.id,
                "trial_index": trial.trial_index,
                "is_correct": out.is_correct,
                "confidence": conf_val,
            })

    if not trial_data:
        raise ValueError(f"Episode {episode_id} has no scored trials to analyze.")

    outcomes = [d["is_correct"] for d in trial_data]
    confidences = [d["confidence"] for d in trial_data]

    # 1. Point estimates
    acc_pt = compute_accuracy(outcomes)
    brier_pt = compute_brier_score(confidences, outcomes)
    ece_pt, cal_bins = compute_expected_calibration_error(confidences, outcomes)
    auroc2_pt = compute_auroc2(confidences, outcomes)
    sdt = compute_type2_sdt(confidences, outcomes)

    # 2. Block bootstrap confidence intervals
    _, acc_low, acc_high = block_bootstrap_ci(
        trial_data,
        lambda sample: compute_accuracy([x["is_correct"] for x in sample]),
        n_resamples=n_bootstraps,
    )
    _, brier_low, brier_high = block_bootstrap_ci(
        trial_data,
        lambda sample: compute_brier_score([x["confidence"] for x in sample], [x["is_correct"] for x in sample]),
        n_resamples=n_bootstraps,
    )
    _, ece_low, ece_high = block_bootstrap_ci(
        trial_data,
        lambda sample: compute_expected_calibration_error([x["confidence"] for x in sample], [x["is_correct"] for x in sample])[0],
        n_resamples=n_bootstraps,
    )
    _, auroc_low, auroc_high = block_bootstrap_ci(
        trial_data,
        lambda sample: compute_auroc2([x["confidence"] for x in sample], [x["is_correct"] for x in sample]),
        n_resamples=n_bootstraps,
    )

    mean_ans_lat = float(np.mean(answer_latencies)) if answer_latencies else None
    mean_conf_lat = float(np.mean(confidence_latencies)) if confidence_latencies else None

    return AnalysisResult(
        episode_id=episode_id,
        protocol_id=episode.protocol_id,
        protocol_version=episode.protocol_version,
        mode=episode.mode,
        n_trials=len(trials),
        n_scored=len(trial_data),
        accuracy=MetricWithCI(round(acc_pt, 4), round(acc_low, 4), round(acc_high, 4)),
        brier_score=MetricWithCI(round(brier_pt, 4), round(brier_low, 4), round(brier_high, 4)),
        ece=MetricWithCI(round(ece_pt, 4), round(ece_low, 4), round(ece_high, 4)),
        auroc2=MetricWithCI(round(auroc2_pt, 4), round(auroc_low, 4), round(auroc_high, 4)),
        d_prime=sdt["d_prime"],
        meta_d_prime=sdt["meta_d_prime"],
        m_ratio=sdt["m_ratio"],
        mean_answer_latency_ms=round(mean_ans_lat, 2) if mean_ans_lat is not None else None,
        mean_confidence_latency_ms=round(mean_conf_lat, 2) if mean_conf_lat is not None else None,
        calibration_bins=cal_bins,
        analyzed_at=datetime.utcnow().isoformat() + "Z",
    )


def generate_analysis_report(
    session: Session,
    episode_id: str,
    app_settings: Settings | None = None,
) -> dict[str, Any]:
    """Execute analysis, generate derived JSON and Markdown report artifacts, and record analysis event."""
    result = analyze_episode(session, episode_id)
    store = ArtifactStore(app_settings)

    # 1. Generate JSON artifact
    json_bytes = json.dumps(asdict(result), indent=2).encode("utf-8")
    json_art = store.save_derived_artifact(
        session=session,
        content=json_bytes,
        mime_type="application/json",
        category="derived/reports",
        filename=f"{episode_id}_analysis.json",
        source_artifact_ids=[],
        processor_version="analysis-kernel-v1.0",
    )

    # 2. Generate Markdown artifact with strict epistemic separation
    md_content = f"""# Project MAMMAL — Session Analysis Report

**Episode ID:** `{result.episode_id}`  
**Protocol:** `{result.protocol_id}` (v{result.protocol_version})  
**Mode:** `{result.mode}`  
**Scored Trials:** {result.n_scored} / {result.n_trials}  
**Analyzed At:** {result.analyzed_at}  

---

## 1. Empirical Estimands (with 95% Block Bootstrap CI)

| Metric | Point Estimate | 95% Empirical CI | Description |
| :--- | :---: | :---: | :--- |
| **Accuracy** | **{result.accuracy.estimate * 100:.1f}%** | [{result.accuracy.ci_lower * 100:.1f}%, {result.accuracy.ci_upper * 100:.1f}%] | First-order proportion correct |
| **Brier Score** | **{result.brier_score.estimate:.4f}** | [{result.brier_score.ci_lower:.4f}, {result.brier_score.ci_upper:.4f}] | Mean quadratic probability loss (lower is better) |
| **Expected Calibration Error (ECE)** | **{result.ece.estimate:.4f}** | [{result.ece.ci_lower:.4f}, {result.ece.ci_upper:.4f}] | Weighted confidence-accuracy gap |
| **Type-2 AUROC (AUROC2)** | **{result.auroc2.estimate:.4f}** | [{result.auroc2.ci_lower:.4f}, {result.auroc2.ci_upper:.4f}] | Metacognitive sensitivity (0.5 = chance, 1.0 = perfect) |

---

## 2. Metacognitive Efficiency & Signal Detection Theory

- **First-order Sensitivity (\(d'\)):** `{result.d_prime:.3f}`
- **Metacognitive Sensitivity (\(meta\\text{{-}}d'\)):** `{result.meta_d_prime:.3f}`
- **Metacognitive Efficiency (\(M_{{ratio}} = \\frac{{meta\\text{{-}}d'}}{{d'}}\)):** `{result.m_ratio:.3f}`

---

## 3. Deliberation Latency

- **Mean Answer Response Latency:** `{result.mean_answer_latency_ms or 'N/A'} ms`
- **Mean Confidence Rating Latency:** `{result.mean_confidence_latency_ms or 'N/A'} ms`

---

## 4. Calibration Bins (Reliability Structure)

| Bin Range | Trial Count | Mean Confidence | Observed Accuracy | Calibration Gap |
| :---: | :---: | :---: | :---: | :---: |
"""
    for b in result.calibration_bins:
        if b["count"] > 0:
            md_content += f"| {b['range'][0]*100:.0f}%–{b['range'][1]*100:.0f}% | {b['count']} | {b['mean_confidence']*100:.1f}% | {b['mean_accuracy']*100:.1f}% | {b['calibration_gap']:+.4f} |\n"
        else:
            md_content += f"| {b['range'][0]*100:.0f}%–{b['range'][1]*100:.0f}% | 0 | — | — | — |\n"

    md_content += """
---

## 5. Epistemic Statement

> Across the currently observed trials under protocol `{0}`, the instrument estimates an empirical first-order accuracy of {1:.1f}% and a metacognitive discrimination AUROC2 of {2:.3f}. These observations reflect performance on the prespecified item set and do not constitute identity-level generalizations.
""".format(result.protocol_id, result.accuracy.estimate * 100, result.auroc2.estimate)

    md_bytes = md_content.encode("utf-8")
    md_art = store.save_derived_artifact(
        session=session,
        content=md_bytes,
        mime_type="text/markdown",
        category="derived/reports",
        filename=f"{episode_id}_summary.md",
        source_artifact_ids=[],
        processor_version="analysis-kernel-v1.0",
    )

    # 3. Log analysis.completed event to event engine
    event_engine = EventEngine(session)
    event_engine.record_event(
        episode_id=episode_id,
        event_type="analysis.completed",
        actor="processor",
        payload={
            "json_artifact_id": json_art.artifact_id,
            "markdown_artifact_id": md_art.artifact_id,
            "accuracy": result.accuracy.estimate,
            "brier_score": result.brier_score.estimate,
            "ece": result.ece.estimate,
            "auroc2": result.auroc2.estimate,
        },
    )

    session.commit()

    return {
        "result": result,
        "json_artifact": json_art,
        "markdown_artifact": md_art,
        "markdown_text": md_content,
    }
