"""Personalized prequential observer models adapting to participant history without leakage."""

from __future__ import annotations

import time
from typing import Any

from mammal.observers.base import ObserverAdapter, ObserverPrediction
from mammal.observers.contracts import VisibilityLevel
from mammal.personalization.history import ParticipantPrequentialHistory


class PersonalizedPrequentialObserver(ObserverAdapter):
    """Personalized observer incorporating causal participant history and calibration traits."""

    @property
    def observer_id(self) -> str:
        return "personalized_prequential"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def visibility_level(self) -> VisibilityLevel:
        return VisibilityLevel.VISIBLE_ANSWER

    def predict(self, compiled_input: dict[str, Any]) -> ObserverPrediction:
        t0 = time.perf_counter()
        domain = str(compiled_input.get("domain") or "semantic")
        answer = str(compiled_input.get("human_locked_answer") or "").strip()
        options = compiled_input.get("options") or []
        latency_ms = float(compiled_input.get("human_response_latency_ms") or 800.0)

        # Retrieve compiled prequential history
        history = compiled_input.get("prequential_history")

        # 1. Base prior probability for item
        base_prob = 0.75 if (options and answer in options) else 0.40

        # 2. Personalized domain mastery adjustment
        if isinstance(history, ParticipantPrequentialHistory) and history.total_prior_trials >= 3:
            dom_acc = history.domain_accuracy.get(domain, history.overall_accuracy)
            # Regress toward domain empirical accuracy
            prob = 0.5 * base_prob + 0.5 * dom_acc

            # 3. Latency anomaly adjustment
            mean_lat = history.mean_latency_ms if history.mean_latency_ms > 0 else 800.0
            if latency_ms > (1.6 * mean_lat):
                prob -= 0.12  # Slow hesitation penalty
            elif latency_ms < (0.7 * mean_lat):
                prob += 0.08  # Rapid fluent retrieval bonus

            # 4. Personalized calibration bias adjustment
            # Map probability to participant's idiosyncratic confidence scale
            bias_offset = history.calibration_bias
            predicted_conf = (prob + bias_offset) * 100.0
        else:
            # Cold-start fallback to generic baseline
            prob = base_prob
            predicted_conf = base_prob * 100.0

        prob = float(max(0.05, min(0.98, prob)))
        predicted_conf = float(max(5.0, min(99.0, predicted_conf)))
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return ObserverPrediction(
            trial_id=compiled_input["trial_id"],
            observer_id=self.observer_id,
            visibility_level=self.visibility_level.value,
            predicted_answer=answer,
            predicted_probability_correct=round(prob, 4),
            confidence=round(predicted_conf, 2),
            latency_ms=round(elapsed_ms, 2),
            raw_metadata={
                "prior_trials_observed": history.total_prior_trials if isinstance(history, ParticipantPrequentialHistory) else 0,
                "domain_accuracy_applied": history.domain_accuracy.get(domain) if isinstance(history, ParticipantPrequentialHistory) else None,
                "calibration_bias_applied": history.calibration_bias if isinstance(history, ParticipantPrequentialHistory) else None,
            },
        )
