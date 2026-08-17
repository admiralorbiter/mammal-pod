"""Unit tests for randomized and Latin-square crossover block assignments."""

from __future__ import annotations

from mammal.interventions.engine import CrossoverBlockAssigner, FeedbackCondition


def test_assign_aba_crossover():
    schedule = CrossoverBlockAssigner.assign_aba_crossover(
        n_blocks=4,
        intervention_condition=FeedbackCondition.MODEL_DISCLOSURE,
    )
    assert len(schedule) == 4
    assert schedule[0] == FeedbackCondition.NO_FEEDBACK
    assert schedule[1] == FeedbackCondition.MODEL_DISCLOSURE
    assert schedule[2] == FeedbackCondition.NO_FEEDBACK
    assert schedule[3] == FeedbackCondition.MODEL_DISCLOSURE


def test_assign_latin_square():
    conditions = [
        FeedbackCondition.NO_FEEDBACK,
        FeedbackCondition.MODEL_DISCLOSURE,
        FeedbackCondition.CALIBRATION_COACHING,
    ]
    p0 = CrossoverBlockAssigner.assign_latin_square(0, conditions)
    p1 = CrossoverBlockAssigner.assign_latin_square(1, conditions)

    assert p0 == conditions
    assert p1 == [
        FeedbackCondition.MODEL_DISCLOSURE,
        FeedbackCondition.CALIBRATION_COACHING,
        FeedbackCondition.NO_FEEDBACK,
    ]
