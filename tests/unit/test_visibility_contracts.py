"""Unit tests for observer visibility contracts and information leakage prevention."""

from __future__ import annotations

from mammal.analysis.manifest import TargetTrialRecord
from mammal.observers.contracts import VisibilityLevel, compile_observer_input


def test_visibility_contract_input_only():
    record = TargetTrialRecord(
        trial_id="trl_test_001",
        trial_index=1,
        item_id="item_geo_01",
        item_version="1.0.0",
        item_content_hash="abc123hash",
        domain="world_geography",
        prompt_payload={"question": "What is the capital of France?"},
        options=["Lyon", "Marseille", "Paris"],
        ground_truth={"canonical": "Paris"},
        human_locked_answer="Paris",
        human_confidence=95.0,
        human_is_correct=True,
        human_score=1.0,
        human_response_latency_ms=650.0,
        human_confidence_latency_ms=400.0,
    )

    compiled = compile_observer_input(record, VisibilityLevel.INPUT_ONLY)

    # Allowed fields
    assert compiled["trial_id"] == "trl_test_001"
    assert compiled["prompt_payload"]["question"] == "What is the capital of France?"
    assert compiled["options"] == ["Lyon", "Marseille", "Paris"]

    # Strictly forbidden fields under INPUT_ONLY
    assert "human_locked_answer" not in compiled
    assert "human_confidence" not in compiled
    assert "human_is_correct" not in compiled
    assert "ground_truth" not in compiled
    assert "human_score" not in compiled
    assert "human_response_latency_ms" not in compiled


def test_visibility_contract_visible_answer():
    record = TargetTrialRecord(
        trial_id="trl_test_002",
        trial_index=2,
        item_id="item_geo_02",
        item_version="1.0.0",
        item_content_hash="def456hash",
        domain="world_geography",
        prompt_payload={"question": "What is the capital of Germany?"},
        options=["Berlin", "Frankfurt", "Munich"],
        ground_truth={"canonical": "Berlin"},
        human_locked_answer="Berlin",
        human_confidence=80.0,
        human_is_correct=True,
        human_score=1.0,
        human_response_latency_ms=750.0,
        human_confidence_latency_ms=350.0,
    )

    compiled = compile_observer_input(record, VisibilityLevel.VISIBLE_ANSWER)

    assert compiled["human_locked_answer"] == "Berlin"
    assert "human_confidence" not in compiled
    assert "ground_truth" not in compiled
    assert "human_is_correct" not in compiled


def test_visibility_contract_visible_confidence():
    record = TargetTrialRecord(
        trial_id="trl_test_003",
        trial_index=3,
        item_id="item_geo_03",
        item_version="1.0.0",
        item_content_hash="ghi789hash",
        domain="world_geography",
        prompt_payload={"question": "What is the capital of Japan?"},
        options=["Osaka", "Tokyo"],
        ground_truth={"canonical": "Tokyo"},
        human_locked_answer="Tokyo",
        human_confidence=99.0,
        human_is_correct=True,
        human_score=1.0,
        human_response_latency_ms=500.0,
        human_confidence_latency_ms=300.0,
    )

    compiled = compile_observer_input(record, VisibilityLevel.VISIBLE_CONFIDENCE)

    assert compiled["human_locked_answer"] == "Tokyo"
    assert compiled["human_confidence"] == 99.0
    assert "ground_truth" not in compiled
    assert "human_is_correct" not in compiled
