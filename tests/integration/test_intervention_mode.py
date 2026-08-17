"""Integration tests for intervention delivery, governance compliance auditing, and effect metrics CLI."""

from __future__ import annotations

from click.testing import CliRunner
from sqlalchemy.orm import Session

from mammal.cli import main
from mammal.config import Settings
from mammal.interventions.engine import FeedbackCondition, deliver_intervention
from mammal.models.entities import Episode, Trial, TrialEvent
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController


def test_full_intervention_workflow_and_governance_cli(temp_settings: Settings, session: Session):
    load_and_register_all_protocols(session)

    controller = SessionController(session)
    participant = controller.get_or_create_participant("Intervention Subject")
    episode = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=6,
    )
    episode_id = episode.id

    # Put episode in intervention mode
    db_episode = session.get(Episode, episode_id)
    db_episode.mode = "intervention"
    session.commit()

    trials = session.query(Trial).filter(Trial.episode_id == episode_id).order_by(Trial.trial_index.asc()).all()

    # 1. Trials 0..2: Baseline unassisted trials (no model intervention)
    for i in range(3):
        t = trials[i]
        item = controller.get_trial_item(t)
        gt = item.ground_truth_json or {}
        correct_canonical = gt.get("canonical", "Paris")

        controller.mark_prompt_shown(t.id)
        is_corr = (i < 2)
        ans = correct_canonical if is_corr else "Wrong Answer"
        controller.lock_answer(t.id, value=ans, modality="button", latency_ms=800.0)
        controller.lock_confidence(t.id, value=95.0 if is_corr else 85.0, modality="numeric", latency_ms=400.0)

    # 2. Trials 3..5: Intervention assisted trials (model disclosure delivered)
    for i in range(3, 6):
        t = trials[i]
        item = controller.get_trial_item(t)
        gt = item.ground_truth_json or {}
        correct_canonical = gt.get("canonical", "Paris")

        controller.mark_prompt_shown(t.id)

        # Deliver approved intervention
        deliver_intervention(
            session=session,
            episode_id=episode_id,
            trial_id=t.id,
            condition=FeedbackCondition.MODEL_DISCLOSURE,
            message="Across currently observed trials, the model estimates a 92% probability of correctness.",
            source_model="mantis_v1",
            source_version="1.0.0",
        )

        controller.lock_answer(t.id, value=correct_canonical, modality="button", latency_ms=450.0)
        controller.lock_confidence(t.id, value=90.0, modality="numeric", latency_ms=250.0)

    session.commit()

    # 3. Verify intervention events in DB
    events = session.query(TrialEvent).filter(TrialEvent.episode_id == episode_id).all()
    interv_events = [e for e in events if e.event_type == "intervention.delivered"]
    assert len(interv_events) == 3

    runner = CliRunner()

    # 4. Test CLI audit-interventions
    res_audit = runner.invoke(
        main,
        ["audit-interventions", episode_id],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_audit.exit_code == 0
    assert "MAMMAL Intervention Governance Audit" in res_audit.output
    assert "COMPLIANT" in res_audit.output

    # 5. Test CLI intervention-effects
    res_effects = runner.invoke(
        main,
        ["intervention-effects", episode_id],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_effects.exit_code == 0
    assert "MAMMAL Intervention Effects" in res_effects.output
    assert "Observation Baseline vs. Intervention Comparison" in res_effects.output
    assert "AGENTS.md Rule 6" in res_effects.output
