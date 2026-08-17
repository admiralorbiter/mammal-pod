"""Unit tests for cued recall text normalization, fuzzy matching, and missing handling."""

from __future__ import annotations

from mammal.memory.recall import score_cued_recall


def test_score_cued_recall_exact_and_case_insensitivity():
    is_corr, score = score_cued_recall("Paris", "paris")
    assert is_corr is True
    assert score == 1.0


def test_score_cued_recall_punctuation_and_whitespace():
    is_corr, score = score_cued_recall("  new   york ! ", "New York")
    assert is_corr is True
    assert score == 1.0


def test_score_cued_recall_acceptable_alternatives():
    is_corr, score = score_cued_recall("USA", "United States", acceptable_alternatives=["US", "USA", "America"])
    assert is_corr is True
    assert score == 1.0


def test_score_cued_recall_missing_and_don_t_know():
    is_corr, score = score_cued_recall("missing", "Berlin")
    assert is_corr is False
    assert score == 0.0

    is_corr, score = score_cued_recall("I don't know", "Berlin")
    assert is_corr is False
    assert score == 0.0
