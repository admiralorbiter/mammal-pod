"""Deterministic scoring engine for Project MAMMAL cognitive trials."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ScoringResult:
    """Canonical outcome of a scored trial."""

    score: float
    is_correct: bool
    scoring_rule: str
    scorer: str = "deterministic_v1"


import re


def normalize_text(text: str) -> str:
    """Normalize text by stripping whitespace, lowercasing, and removing punctuation."""
    t = str(text).strip().lower()
    t = re.sub(r"[^\w\s]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def score_trial_answer(locked_answer_value: Any, ground_truth: Any) -> ScoringResult:
    """Score a locked participant response against ground truth.

    Supports:
    - Dict with 'option_index' matching
    - Dict with 'canonical' string matching
    - Direct integer index matching
    - Direct string matching
    """
    if isinstance(ground_truth, dict):
        canonical_str = ground_truth.get("canonical")
        gt_index = ground_truth.get("option_index")

        # Case 1: Answer is dict with option_index
        if isinstance(locked_answer_value, dict) and "option_index" in locked_answer_value:
            user_idx = locked_answer_value["option_index"]
            if gt_index is not None:
                is_correct = int(user_idx) == int(gt_index)
                return ScoringResult(
                    score=1.0 if is_correct else 0.0,
                    is_correct=is_correct,
                    scoring_rule="option_index_match",
                )

        # Case 2: Answer is an integer index
        if isinstance(locked_answer_value, int) and gt_index is not None:
            is_correct = locked_answer_value == gt_index
            return ScoringResult(
                score=1.0 if is_correct else 0.0,
                is_correct=is_correct,
                scoring_rule="option_index_match",
            )

        # Case 3: Answer is dict with string value
        if isinstance(locked_answer_value, dict) and "value" in locked_answer_value:
            user_str = str(locked_answer_value["value"])
            if canonical_str is not None:
                is_correct = normalize_text(user_str) == normalize_text(canonical_str)
                return ScoringResult(
                    score=1.0 if is_correct else 0.0,
                    is_correct=is_correct,
                    scoring_rule="normalized_string_match",
                )

        # Case 4: Answer is raw string
        if isinstance(locked_answer_value, str) and canonical_str is not None:
            is_correct = normalize_text(locked_answer_value) == normalize_text(canonical_str)
            return ScoringResult(
                score=1.0 if is_correct else 0.0,
                is_correct=is_correct,
                scoring_rule="normalized_string_match",
            )

    # Fallback direct string / equality match
    if isinstance(locked_answer_value, str) and isinstance(ground_truth, str):
        is_correct = normalize_text(locked_answer_value) == normalize_text(ground_truth)
        return ScoringResult(
            score=1.0 if is_correct else 0.0,
            is_correct=is_correct,
            scoring_rule="normalized_string_match",
        )

    is_correct = locked_answer_value == ground_truth
    return ScoringResult(
        score=1.0 if is_correct else 0.0,
        is_correct=is_correct,
        scoring_rule="direct_equality",
    )
