"""Observer visibility contracts and input compilation for Project MAMMAL."""

from __future__ import annotations

from enum import Enum
from typing import Any

from mammal.analysis.manifest import TargetTrialRecord


class VisibilityLevel(str, Enum):
    INPUT_ONLY = "INPUT_ONLY"  # Item prompt and options only
    VISIBLE_ANSWER = "VISIBLE_ANSWER"  # Item prompt + participant's locked answer
    VISIBLE_CONFIDENCE = "VISIBLE_CONFIDENCE"  # Item + answer + participant's locked confidence
    PROMPT_PLUS_SPEECH = "PROMPT_PLUS_SPEECH"  # Item + speech audio/transcript
    FULL_RECORDING = "FULL_RECORDING"  # Complete trial telemetry


def compile_observer_input(
    record: TargetTrialRecord,
    visibility: VisibilityLevel,
) -> dict[str, Any]:
    """Compile trial input for an observer, strictly filtering out information forbidden by its contract."""
    # Base input (permitted under all visibility levels)
    compiled: dict[str, Any] = {
        "trial_id": record.trial_id,
        "trial_index": record.trial_index,
        "item_id": record.item_id,
        "domain": record.domain,
        "prompt_payload": record.prompt_payload,
        "options": record.options,
    }

    if visibility == VisibilityLevel.INPUT_ONLY:
        # Absolutely NO human response, confidence, ground truth, or latency
        return compiled

    if visibility in (VisibilityLevel.VISIBLE_ANSWER, VisibilityLevel.VISIBLE_CONFIDENCE, VisibilityLevel.FULL_RECORDING):
        compiled["human_locked_answer"] = record.human_locked_answer

    if visibility in (VisibilityLevel.VISIBLE_CONFIDENCE, VisibilityLevel.FULL_RECORDING):
        compiled["human_confidence"] = record.human_confidence

    if visibility in (VisibilityLevel.PROMPT_PLUS_SPEECH, VisibilityLevel.FULL_RECORDING):
        compiled["human_locked_answer"] = record.human_locked_answer
        compiled["human_response_latency_ms"] = record.human_response_latency_ms

    if visibility == VisibilityLevel.FULL_RECORDING:
        compiled["human_confidence_latency_ms"] = record.human_confidence_latency_ms

    return compiled
