"""Integration tests for the statistical analysis pipeline, artifact generation, and CLI."""

from __future__ import annotations

import json
from pathlib import Path
import pytest
from click.testing import CliRunner
from sqlalchemy.orm import Session

from mammal.analysis.engine import analyze_episode, generate_analysis_report
from mammal.artifacts.store import ArtifactStore
from mammal.cli import main
from mammal.config import Settings
from mammal.models.entities import Episode, Trial, TrialEvent
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController


def test_full_analysis_pipeline_and_artifacts(session: Session, temp_settings: Settings):
    load_and_register_all_protocols(session)
    controller = SessionController(session)
    participant = controller.get_or_create_participant("Analysis Test Subject")

    episode = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=10,
    )
    episode_id = episode.id

    trials = session.query(Trial).filter(Trial.episode_id == episode_id).all()
    assert len(trials) == 10

    # Execute 7 correct and 3 incorrect trials
    for i, trial in enumerate(trials):
        item = controller.get_trial_item(trial)
        gt = item.ground_truth_json or {}
        correct_canonical = gt.get("canonical", "Paris")

        controller.mark_prompt_shown(trial.id)
        is_correct = (i < 7)
        ans_val = correct_canonical if is_correct else "Wrong Answer"
        conf_val = 90.0 if is_correct else 30.0

        controller.lock_answer(trial.id, value=ans_val, modality="button", latency_ms=650)
        controller.lock_confidence(trial.id, value=conf_val, modality="numeric", latency_ms=450)

    session.commit()

    # 1. Run analysis and generate reports
    report_data = generate_analysis_report(session, episode_id, app_settings=temp_settings)
    res = report_data["result"]
    json_art = report_data["json_artifact"]
    md_art = report_data["markdown_artifact"]
    md_text = report_data["markdown_text"]

    # 2. Verify numerical estimands
    assert res.accuracy.estimate == pytest.approx(0.70, abs=1e-3)
    assert 0.0 < res.brier_score.estimate < 0.25
    assert res.auroc2.estimate == 1.0  # Perfect separation: 90% on correct vs 30% on incorrect

    # 3. Verify artifact store integrity
    store = ArtifactStore(temp_settings)
    assert store.verify_artifact(session, json_art.artifact_id) is True
    assert store.verify_artifact(session, md_art.artifact_id) is True

    # 4. Verify Epistemic statement rules in markdown
    assert "Across the currently observed trials under protocol" in md_text
    assert "inherently" not in md_text.lower()

    # 5. Verify analysis.completed event recorded
    analysis_ev = (
        session.query(TrialEvent)
        .filter(TrialEvent.episode_id == episode_id, TrialEvent.event_type == "analysis.completed")
        .first()
    )
    assert analysis_ev is not None
    assert analysis_ev.payload_json["json_artifact_id"] == json_art.artifact_id


def test_cli_analyze_command(temp_settings: Settings, session: Session):
    load_and_register_all_protocols(session)
    controller = SessionController(session)
    participant = controller.get_or_create_participant("CLI Analysis User")
    episode = controller.start_session(
        protocol_id="e00_instrument_qualification",
        participant_id=participant.id,
        item_limit=4,
    )

    for trial in session.query(Trial).filter(Trial.episode_id == episode.id).all():
        item = controller.get_trial_item(trial)
        gt = item.ground_truth_json or {}
        correct_canonical = gt.get("canonical", "Paris")

        controller.mark_prompt_shown(trial.id)
        controller.lock_answer(trial.id, value=correct_canonical, modality="button")
        controller.lock_confidence(trial.id, value=80.0, modality="numeric")
    session.commit()

    runner = CliRunner()

    # Test default text table format
    res_text = runner.invoke(
        main,
        ["analyze", episode.id],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_text.exit_code == 0
    assert "MAMMAL Statistical Analysis" in res_text.output
    assert "Accuracy" in res_text.output

    # Test JSON output format
    res_json = runner.invoke(
        main,
        ["analyze", episode.id, "--format", "json"],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_json.exit_code == 0
    parsed = json.loads(res_json.output)
    assert parsed["episode_id"] == episode.id
    assert parsed["accuracy"]["estimate"] == 1.0

    # Test Markdown output format
    res_md = runner.invoke(
        main,
        ["analyze", episode.id, "--format", "markdown"],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_md.exit_code == 0
    assert "# Project MAMMAL — Session Analysis Report" in res_md.output
