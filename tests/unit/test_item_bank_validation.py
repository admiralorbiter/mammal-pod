"""Unit tests for ItemValidator, option homogeneity, and partition isolation."""

from __future__ import annotations

import pytest

from mammal.items.validator import ItemValidator


@pytest.fixture
def validator() -> ItemValidator:
    return ItemValidator()


def test_valid_item_passes(validator: ItemValidator):
    valid_item = {
        "item_id": "test_001",
        "version": "1.0.0",
        "domain": "semantic",
        "family": "general_knowledge",
        "prompt": {"question": "What is the capital of France?"},
        "options": ["Lyon", "Marseille", "Paris", "Nice"],
        "ground_truth": {"canonical": "Paris", "option_index": 2},
        "partition": "confirmatory",
        "source": {"provenance": "test_fixture", "license": "CC0"},
    }
    errors, warnings = validator.validate_item(valid_item)
    assert len(errors) == 0


def test_missing_required_fields_fails(validator: ItemValidator):
    invalid_item = {
        "item_id": "test_invalid_001",
        "domain": "semantic",
        # missing version, family, prompt, ground_truth, partition, source
    }
    errors, _ = validator.validate_item(invalid_item)
    assert len(errors) > 0
    assert any("Schema violation" in err.message for err in errors)


def test_duplicate_options_detected(validator: ItemValidator):
    dup_item = {
        "item_id": "test_dup_opt",
        "version": "1.0.0",
        "domain": "semantic",
        "family": "general_knowledge",
        "prompt": {"question": "Choose A or B"},
        "options": ["Option A", "Option B", "option a"],
        "ground_truth": {"canonical": "Option B", "option_index": 1},
        "partition": "exploratory",
        "source": {"provenance": "test_fixture"},
    }
    errors, _ = validator.validate_item(dup_item)
    assert any("duplicate choices" in err.message for err in errors)


def test_ground_truth_mismatch_detected(validator: ItemValidator):
    mismatch_item = {
        "item_id": "test_mismatch",
        "version": "1.0.0",
        "domain": "semantic",
        "family": "general_knowledge",
        "prompt": {"question": "What is 2+2?"},
        "options": ["3", "4", "5", "6"],
        "ground_truth": {"canonical": "4", "option_index": 0},  # index 0 is "3"
        "partition": "exploratory",
        "source": {"provenance": "test_fixture"},
    }
    errors, _ = validator.validate_item(mismatch_item)
    assert any("does not match canonical" in err.message for err in errors)


def test_cross_partition_prompt_collision_detected(validator: ItemValidator):
    items = [
        {
            "item_id": "item_exploratory",
            "version": "1.0.0",
            "domain": "semantic",
            "family": "general_knowledge",
            "prompt": {"question": "What is the boiling point of water?"},
            "options": ["90C", "100C", "110C", "120C"],
            "ground_truth": {"canonical": "100C", "option_index": 1},
            "partition": "exploratory",
            "source": {"provenance": "test_fixture"},
        },
        {
            "item_id": "item_confirmatory",
            "version": "1.0.0",
            "domain": "semantic",
            "family": "general_knowledge",
            "prompt": {"question": "What is the boiling point of water?"},  # identical prompt
            "options": ["90C", "100C", "110C", "120C"],
            "ground_truth": {"canonical": "100C", "option_index": 1},
            "partition": "confirmatory",  # different partition -> collision!
            "source": {"provenance": "test_fixture"},
        },
    ]
    report = validator.validate_items(items)
    assert not report.is_valid
    assert any("Prompt collision across partitions" in err.message for err in report.errors)
