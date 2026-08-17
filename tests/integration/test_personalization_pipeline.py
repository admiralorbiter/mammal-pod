"""Integration tests for prequential history compilation, personalized model execution, and gain CLI."""

from __future__ import annotations

from click.testing import CliRunner
from sqlalchemy.orm import Session

from mammal.cli import main
from mammal.config import Settings
from mammal.models.entities import Trial
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController


def test_full_personalization_pipeline_and_gain_cli(temp_settings: Settings, session: Session):
    load_and_register_all_protocols(session)

    controller = SessionController(session)
    participant = controller.get_or_create_participant("Prequential Subject")

    # 1. Episode 1: Build initial 4 trials of participant history
    ep1 = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=4,
    )
    trials_ep1 = session.query(Trial).filter(Trial.episode_id == ep1.id).order_by(Trial.trial_index.asc()).all()
    for i, t in enumerate(trials_ep1):
        item = controller.get_trial_item(t)
        gt = item.ground_truth_json or {}
        correct_canonical = gt.get("canonical", "Paris")

        controller.mark_prompt_shown(t.id)
        is_corr = (i < 3)
        ans = correct_canonical if is_corr else "Wrong Answer"
        controller.lock_answer(t.id, value=ans, modality="button", latency_ms=600.0)
        controller.lock_confidence(t.id, value=85.0 if is_corr else 30.0, modality="numeric", latency_ms=300.0)

    session.commit()

    # 2. Episode 2: Second session evaluating personalization gain
    ep2 = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=4,
    )
    trials_ep2 = session.query(Trial).filter(Trial.episode_id == ep2.id).order_by(Trial.trial_index.asc()).all()
    for i, t in enumerate(trials_ep2):
        item = controller.get_trial_item(t)
        gt = item.ground_truth_json or {}
        correct_canonical = gt.get("canonical", "Paris")

        controller.mark_prompt_shown(t.id)
        is_corr = (i < 3)
        ans = correct_canonical if is_corr else "Wrong Answer"
        controller.lock_answer(t.id, value=ans, modality="button", latency_ms=550.0)
        controller.lock_confidence(t.id, value=90.0 if is_corr else 25.0, modality="numeric", latency_ms=350.0)

    session.commit()

    runner = CliRunner()

    # 3. Run CLI personalize on Episode 2
    res_pers = runner.invoke(
        main,
        ["personalize", ep2.id],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_pers.exit_code == 0
    assert "MAMMAL Personalized Prequential Observer" in res_pers.output
    assert "Completed 4 personalized trial predictions" in res_pers.output

    # 4. Run CLI personalization-gain on Episode 2
    res_gain = runner.invoke(
        main,
        ["personalization-gain", ep2.id],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_gain.exit_code == 0
    assert "MAMMAL Personalization Gain" in res_gain.output
    assert "Personalized" in res_gain.output
    assert "Prequential" in res_gain.output
    assert "Across the currently observed trials" in res_gain.output
