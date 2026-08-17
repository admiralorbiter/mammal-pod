"""Unit tests for deterministic scoring engine."""

from __future__ import annotations

from mammal.scoring.engine import score_trial_answer


def test_exact_string_scoring():
    gt = {"canonical": "Paris", "option_index": 2}

    res_correct = score_trial_answer("Paris", gt)
    assert res_correct.is_correct is True
    assert res_correct.score == 1.0

    res_case_insens = score_trial_answer("  paris  ", gt)
    assert res_case_insens.is_correct is True
    assert res_case_insens.score == 1.0

    res_incorrect = score_trial_answer("Lyon", gt)
    assert res_incorrect.is_correct is False
    assert res_incorrect.score == 0.0


def test_option_index_scoring():
    gt = {"canonical": "Paris", "option_index": 2}

    res_correct = score_trial_answer(2, gt)
    assert res_correct.is_correct is True
    assert res_correct.score == 1.0
    assert res_correct.scoring_rule == "option_index_match"

    res_incorrect = score_trial_answer(0, gt)
    assert res_incorrect.is_correct is False
    assert res_incorrect.score == 0.0


def test_dict_answer_scoring():
    gt = {"canonical": "Paris", "option_index": 2}

    res_idx = score_trial_answer({"option_index": 2}, gt)
    assert res_idx.is_correct is True
    assert res_idx.score == 1.0

    res_val = score_trial_answer({"value": "Paris"}, gt)
    assert res_val.is_correct is True
    assert res_val.score == 1.0
