"""Integration tests for observer runner, visibility contract compliance, and paired evaluation CLI."""

from __future__ import annotations

from click.testing import CliRunner
from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore
from mammal.cli import main
from mammal.config import Settings
from mammal.models.entities import Trial, TrialEvent
from mammal.observers.runner import get_observer, run_observer_on_episode
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController


def test_full_observer_pipeline_and_paired_comparison(temp_settings: Settings, session: Session):
    load_and_register_all_protocols(session)

    controller = SessionController(session)
    participant = controller.get_or_create_participant("Observer Ladder Subject")
    episode = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=6,
    )
    episode_id = episode.id

    # 1. Execute trials with participant answers and confidence
    trials = session.query(Trial).filter(Trial.episode_id == episode_id).all()
    for i, trial in enumerate(trials):
        item = controller.get_trial_item(trial)
        gt = item.ground_truth_json or {}
        correct_canonical = gt.get("canonical", "Paris")

        controller.mark_prompt_shown(trial.id)
        is_correct = (i % 2 == 0)
        ans_val = correct_canonical if is_correct else "Wrong Answer"
        conf_val = 85.0 if is_correct else 35.0

        controller.lock_answer(trial.id, value=ans_val, modality="button", latency_ms=550)
        controller.lock_confidence(trial.id, value=conf_val, modality="numeric", latency_ms=350)

    session.commit()

    # 2. Run ItemBaseRateObserver programmatically
    obs = get_observer("item_base_rate")
    run_res = run_observer_on_episode(session, episode_id, obs, app_settings=temp_settings)
    assert len(run_res["predictions"]) == 6
    assert run_res["paired_result"] is not None

    # 3. Verify observer events in DB
    events = session.query(TrialEvent).filter(TrialEvent.episode_id == episode_id).all()
    obs_events = [e for e in events if e.event_type == "observer.prediction_locked"]
    assert len(obs_events) == 6

    # 4. Verify artifact store integrity
    store = ArtifactStore(temp_settings)
    art = run_res["artifact"]
    content = store.read_artifact_bytes(session, art.artifact_id)
    assert b"item_base_rate" in content

    runner = CliRunner()

    # 5. Test CLI observe
    res_observe = runner.invoke(
        main,
        ["observe", episode_id, "--observer", "item_base_rate"],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_observe.exit_code == 0
    assert "MAMMAL Observer Evaluation" in res_observe.output
    assert "Completed 6 trial predictions" in res_observe.output

    # 6. Test CLI compare
    res_compare = runner.invoke(
        main,
        ["compare", episode_id, "--observer", "item_base_rate"],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_compare.exit_code == 0
    assert "MAMMAL Paired Comparison" in res_compare.output
    assert "PAI" in res_compare.output
    assert "Advantage Index" in res_compare.output
