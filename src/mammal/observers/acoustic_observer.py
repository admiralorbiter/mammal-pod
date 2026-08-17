"""Acoustic prosody observer predicting human accuracy and confidence from vocal features."""

from __future__ import annotations

import time
from typing import Any

from mammal.observers.base import ObserverAdapter, ObserverPrediction
from mammal.observers.contracts import VisibilityLevel
from mammal.processors.acoustics import extract_acoustic_features


class AcousticProsodyObserver(ObserverAdapter):
    """Observer under PROMPT_PLUS_SPEECH predicting metacognitive confidence from speech acoustics."""

    @property
    def observer_id(self) -> str:
        return "acoustic_prosody"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def visibility_level(self) -> VisibilityLevel:
        return VisibilityLevel.PROMPT_PLUS_SPEECH

    def predict(self, compiled_input: dict[str, Any]) -> ObserverPrediction:
        t0 = time.perf_counter()
        answer = str(compiled_input.get("human_locked_answer") or "").strip()
        latency_ms = float(compiled_input.get("human_response_latency_ms") or 800.0)
        acoustic_meta = compiled_input.get("acoustic_features") or {}

        # Base confidence
        conf = 75.0

        # 1. Latency penalty (hesitation delay > 1200ms)
        if latency_ms > 2000.0:
            conf -= 25.0
        elif latency_ms > 1200.0:
            conf -= 15.0
        elif latency_ms < 700.0:
            conf += 10.0

        # 2. Prosodic acoustic feature adjustments (if audio features were extracted)
        rising_terminal = acoustic_meta.get("rising_terminal_pitch", False)
        jitter = float(acoustic_meta.get("pitch_jitter_pct") or 2.0)
        shimmer = float(acoustic_meta.get("shimmer_pct") or 3.0)

        if rising_terminal:
            # Uptalk / questioning tone indicates uncertainty
            conf -= 25.0

        if jitter > 6.0:
            # Pitch instability / vocal tremor indicates hesitation
            conf -= 15.0

        if shimmer > 8.0:
            # Amplitude instability
            conf -= 10.0

        conf = float(max(10.0, min(98.0, conf)))
        prob = float(conf / 100.0)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return ObserverPrediction(
            trial_id=compiled_input["trial_id"],
            observer_id=self.observer_id,
            visibility_level=self.visibility_level.value,
            predicted_answer=answer,
            predicted_probability_correct=round(prob, 4),
            confidence=round(conf, 2),
            latency_ms=round(elapsed_ms, 2),
            raw_metadata={
                "rising_terminal_pitch": rising_terminal,
                "pitch_jitter_pct": jitter,
                "latency_penalty_applied": latency_ms > 1200.0,
            },
        )
