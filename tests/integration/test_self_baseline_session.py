"""Integration tests for Human Self baseline session, precision planning, and manifest freezing."""

from __future__ import annotations

from click.testing import CliRunner
from sqlalchemy.orm import Session

from mammal.cli import main
from mammal.config import Settings
from mammal.models.entities import Episode, Trial
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController
from mammal.trials.scheduler import DomainSessionScheduler


def test_full_self_baseline_and_manifest_workflow(temp_settings: Settings, session: Session):
    load_and_register_all_protocols(session)

    # 1. Schedule multi-domain session plan
    scheduler = DomainSessionScheduler(session)
    domains = ["world_geography", "propositional_logic"]
    plan = scheduler.plan_session(
        protocol_id="e00_instrument_qualification",
        domains=domains,
        items_per_domain=4,
        block_size=2,
    )
    assert plan.total_trials == 8

    # 2. Start session with controller
    controller = SessionController(session)
    participant = controller.get_or_create_participant("Self Baseline Subject")
    episode = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=8,
    )
    episode_id = episode.id

    # 3. Execute all 8 trials with human responses
    trials = session.query(Trial).filter(Trial.episode_id == episode_id).all()
    for i, trial in enumerate(trials):
        item = controller.get_trial_item(trial)
        gt = item.ground_truth_json or {}
        correct_canonical = gt.get("canonical", "Paris")

        controller.mark_prompt_shown(trial.id)
        is_correct = (i < 6)  # 6 correct, 2 incorrect -> 75% accuracy
        ans_val = correct_canonical if is_correct else "Wrong Answer"
        conf_val = 80.0 if is_correct else 30.0

        controller.lock_answer(trial.id, value=ans_val, modality="button", latency_ms=600)
        controller.lock_confidence(trial.id, value=conf_val, modality="numeric", latency_ms=400)

    session.commit()

    runner = CliRunner()

    # 4. Test CLI plan-precision
    res_plan = runner.invoke(main, ["plan-precision", "--metric", "brier", "--ci-half-width", "0.06"])
    assert res_plan.exit_code == 0
    assert "MAMMAL Precision Planner" in res_plan.output
    assert "Recommended minimum sample size" in res_plan.output

    # 5. Test CLI freeze-manifest
    res_freeze = runner.invoke(
        main,
        ["freeze-manifest", episode_id],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_freeze.exit_code == 0
    assert "Target Manifest Frozen Successfully" in res_freeze.output
    assert "Manifest SHA-256 Digest" in res_freeze.output

    # 6. Test CLI analyze
    res_analyze = runner.invoke(
        main,
        ["analyze", episode_id],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_analyze.exit_code == 0
    assert "Accuracy" in res_analyze.output
    assert "75.0%" in res_analyze.output
