"""Generic and statistical baseline observers for Project MAMMAL."""

from __future__ import annotations

import time
from typing import Any

from mammal.observers.base import ObserverAdapter, ObserverPrediction
from mammal.observers.contracts import VisibilityLevel


class UniformChanceObserver(ObserverAdapter):
    """Chance baseline predicting uniform random choice with flat confidence."""

    @property
    def observer_id(self) -> str:
        return "uniform_chance"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def visibility_level(self) -> VisibilityLevel:
        return VisibilityLevel.INPUT_ONLY

    def predict(self, compiled_input: dict[str, Any]) -> ObserverPrediction:
        t0 = time.perf_counter()
        options = compiled_input.get("options") or []
        k = len(options) if options else 2
        prob = 1.0 / k
        conf = prob * 100.0
        predicted_ans = options[0] if options else "unknown"
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return ObserverPrediction(
            trial_id=compiled_input["trial_id"],
            observer_id=self.observer_id,
            visibility_level=self.visibility_level.value,
            predicted_answer=predicted_ans,
            predicted_probability_correct=round(prob, 4),
            confidence=round(conf, 2),
            latency_ms=round(elapsed_ms, 2),
            raw_metadata={"num_options": k},
        )


class ItemBaseRateObserver(ObserverAdapter):
    """Empirical domain difficulty baseline predicting historical accuracy base rates."""

    DOMAIN_BASE_RATES: dict[str, float] = {
        "semantic": 0.75,
        "world_geography": 0.78,
        "physical_science": 0.72,
        "formal_math_logic": 0.65,
        "propositional_logic": 0.62,
        "arithmetic": 0.80,
        "perception_rdk": 0.70,
    }

    def __init__(self, default_rate: float = 0.70) -> None:
        self.default_rate = default_rate

    @property
    def observer_id(self) -> str:
        return "item_base_rate"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def visibility_level(self) -> VisibilityLevel:
        return VisibilityLevel.INPUT_ONLY

    def predict(self, compiled_input: dict[str, Any]) -> ObserverPrediction:
        t0 = time.perf_counter()
        domain = compiled_input.get("domain", "")
        prob = self.DOMAIN_BASE_RATES.get(domain, self.default_rate)
        conf = prob * 100.0
        options = compiled_input.get("options") or []
        predicted_ans = options[0] if options else "base_rate_prediction"
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return ObserverPrediction(
            trial_id=compiled_input["trial_id"],
            observer_id=self.observer_id,
            visibility_level=self.visibility_level.value,
            predicted_answer=predicted_ans,
            predicted_probability_correct=round(prob, 4),
            confidence=round(conf, 2),
            latency_ms=round(elapsed_ms, 2),
            raw_metadata={"domain": domain, "assigned_base_rate": prob},
        )


class DeterministicSolverObserver(ObserverAdapter):
    """Direct solver model that attempts to resolve questions via knowledge heuristics."""

    @property
    def observer_id(self) -> str:
        return "deterministic_solver"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def visibility_level(self) -> VisibilityLevel:
        return VisibilityLevel.INPUT_ONLY

    def predict(self, compiled_input: dict[str, Any]) -> ObserverPrediction:
        t0 = time.perf_counter()
        prompt = compiled_input.get("prompt_payload") or {}
        q_text = prompt.get("question", "").lower()
        options = compiled_input.get("options") or []

        # Simple deterministic geography & logic heuristics
        predicted_ans = options[0] if options else "none"
        prob = 0.70

        if "france" in q_text and "Paris" in options:
            predicted_ans = "Paris"
            prob = 0.95
        elif "germany" in q_text and "Berlin" in options:
            predicted_ans = "Berlin"
            prob = 0.95
        elif "japan" in q_text and "Tokyo" in options:
            predicted_ans = "Tokyo"
            prob = 0.95
        elif "gold" in q_text and "Au" in options:
            predicted_ans = "Au"
            prob = 0.95
        elif "modus ponens" in q_text and "Valid" in options:
            predicted_ans = "Valid"
            prob = 0.90

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return ObserverPrediction(
            trial_id=compiled_input["trial_id"],
            observer_id=self.observer_id,
            visibility_level=self.visibility_level.value,
            predicted_answer=predicted_ans,
            predicted_probability_correct=round(prob, 4),
            confidence=round(prob * 100.0, 2),
            latency_ms=round(elapsed_ms, 2),
            raw_metadata={"solver_strategy": "deterministic_rule_lookup"},
        )


class TextConfidenceHeuristicObserver(ObserverAdapter):
    """Observer with VISIBLE_ANSWER contract estimating correctness from human answer text and format."""

    @property
    def observer_id(self) -> str:
        return "text_confidence_heuristic"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def visibility_level(self) -> VisibilityLevel:
        return VisibilityLevel.VISIBLE_ANSWER

    def predict(self, compiled_input: dict[str, Any]) -> ObserverPrediction:
        t0 = time.perf_counter()
        answer = str(compiled_input.get("human_locked_answer") or "").strip()
        options = compiled_input.get("options") or []

        # If human gave a non-empty answer matching options, assign higher correctness probability
        if options and answer in options:
            prob = 0.82
        elif len(answer) > 0 and answer != "Wrong Answer":
            prob = 0.75
        else:
            prob = 0.35

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return ObserverPrediction(
            trial_id=compiled_input["trial_id"],
            observer_id=self.observer_id,
            visibility_level=self.visibility_level.value,
            predicted_answer=answer,
            predicted_probability_correct=round(prob, 4),
            confidence=round(prob * 100.0, 2),
            latency_ms=round(elapsed_ms, 2),
            raw_metadata={"answer_evaluated": answer},
        )
