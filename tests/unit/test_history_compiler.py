"""Unit tests for prequential history compiler and zero-future-leakage guarantees."""

from __future__ import annotations

from sqlalchemy.orm import Session

from mammal.config import Settings
from mammal.models.entities import Episode, Trial
from mammal.personalization.history import compile_prequential_history
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController


def test_prequential_history_zero_future_leakage(temp_settings: Settings, session: Session):
    load_and_register_all_protocols(session)

    controller = SessionController(session)
    participant = controller.get_or_create_participant("History Test Subject")
    episode = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=6,
    )
    episode_id = episode.id

    trials = session.query(Trial).filter(Trial.episode_id == episode_id).order_by(Trial.trial_index.asc()).all()

    # Complete trials 1 to 4
    for i in range(4):
        t = trials[i]
        controller.mark_prompt_shown(t.id)
        controller.lock_answer(t.id, value="Paris", modality="button", latency_ms=600.0)
        controller.lock_confidence(t.id, value=90.0, modality="numeric", latency_ms=300.0)

    session.commit()

    # Target trial is trial 3 (index 3, 4th trial in 0-indexed list)
    target_trial_3 = trials[2]
    history_at_3 = compile_prequential_history(session, participant.id, target_trial_3.id)

    # Must contain strictly trials 0 and 1 (2 prior trials)
    assert history_at_3.total_prior_trials == 2
    history_ids = [h.trial_id for h in history_at_3.history_trials]
    assert trials[0].id in history_ids
    assert trials[1].id in history_ids
    # Target trial 3 and subsequent trial 4 MUST NOT appear
    assert trials[2].id not in history_ids
    assert trials[3].id not in history_ids


def test_prequential_history_calibration_bias(temp_settings: Settings, session: Session):
    load_and_register_all_protocols(session)

    controller = SessionController(session)
    participant = controller.get_or_create_participant("Overconfident Subject")
    episode = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=5,
    )
    trials = session.query(Trial).filter(Trial.episode_id == episode.id).order_by(Trial.trial_index.asc()).all()

    # Complete 4 trials: 2 correct with 90% conf, 2 incorrect with 90% conf (50% acc, 90% conf -> +0.40 calibration bias)
    for i in range(4):
        t = trials[i]
        item = controller.get_trial_item(t)
        gt = item.ground_truth_json or {}
        correct_canonical = gt.get("canonical", "Paris")

        controller.mark_prompt_shown(t.id)
        is_corr = (i < 2)
        ans = correct_canonical if is_corr else "Wrong Answer"
        controller.lock_answer(t.id, value=ans, modality="button", latency_ms=700.0)
        controller.lock_confidence(t.id, value=90.0, modality="numeric", latency_ms=300.0)

    session.commit()

    history = compile_prequential_history(session, participant.id, trials[4].id)
    assert history.total_prior_trials == 4
    assert history.overall_accuracy == 0.50
    assert history.mean_reported_confidence == 90.0
    # Overconfidence bias: 0.90 - 0.50 = +0.40
    assert history.calibration_bias == 0.40
