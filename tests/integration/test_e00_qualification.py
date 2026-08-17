"""Integration tests for the 100-trial E00 instrument qualification protocol and deterministic replay."""

from __future__ import annotations

import pytest
from click.testing import CliRunner
from sqlalchemy.orm import Session

from mammal.cli import main
from mammal.config import Settings
from mammal.db import get_session
from mammal.items.qualification import seed_e00_qualification_items
from mammal.models.entities import Episode, Trial
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController
from mammal.trials.replay import replay_session_from_events


def test_full_100_trial_e00_qualification_and_replay(session: Session, temp_settings: Settings):
    # 1. Register protocol and seed 100 qualification items
    load_and_register_all_protocols(session)
    seed_e00_qualification_items(session)
    session.commit()

    controller = SessionController(session)
    participant = controller.get_or_create_participant("Qualification Pilot Jonathan")

    # 2. Start full 100-trial qualification episode
    episode = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=100,
    )
    episode_id = episode.id

    # Verify 100 trials scheduled
    trials = session.query(Trial).filter(Trial.episode_id == episode_id).all()
    assert len(trials) == 100

    # 3. Simulate sequential trial execution
    for i, trial in enumerate(trials, start=1):
        item = controller.get_trial_item(trial)
        gt = item.ground_truth_json or {}
        correct_ans = gt.get("canonical", "Paris")

        # Mix of correct and incorrect responses with varied confidence
        is_correct_sim = (i % 5 != 0)  # 80% simulated accuracy
        ans_val = correct_ans if is_correct_sim else "Incorrect Answer"
        conf_val = 85.0 if is_correct_sim else 30.0

        controller.mark_prompt_shown(trial.id)
        controller.lock_answer(trial.id, value=ans_val, modality="button", latency_ms=800 + (i % 200))
        controller.lock_confidence(trial.id, value=conf_val, modality="numeric", latency_ms=500 + (i % 100))

    session.commit()

    # 4. Verify episode completed
    session.refresh(episode)
    assert episode.status == "completed"
    assert episode.ended_at is not None

    # 5. Execute deterministic session replay across all 100 trials
    summary = replay_session_from_events(
        session=session,
        episode_id=episode_id,
        app_settings=temp_settings,
    )

    assert summary.is_valid is True
    assert summary.total_trials == 100
    assert summary.replayed_trials == 100
    assert summary.total_events >= 600  # >= 6 events per trial
    assert len(summary.discrepancies) == 0


def test_cli_replay_command(temp_settings: Settings, session: Session):
    # Setup short episode
    load_and_register_all_protocols(session)
    controller = SessionController(session)
    participant = controller.get_or_create_participant("CLI Test User")
    episode = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=3,
    )

    for trial in session.query(Trial).filter(Trial.episode_id == episode.id).all():
        controller.mark_prompt_shown(trial.id)
        controller.lock_answer(trial.id, value="Paris", modality="button")
        controller.lock_confidence(trial.id, value=75.0, modality="numeric")
    session.commit()

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["replay", episode.id],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert result.exit_code == 0
    assert "Session Replay Audit" in result.output
    assert "PASS" in result.output
