"""Integration tests for memory encoding, JOL lock, cued recall, and prospective analysis CLI."""

from __future__ import annotations

from click.testing import CliRunner
from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore
from mammal.cli import main
from mammal.config import Settings
from mammal.memory.encoding import record_encoding_jol
from mammal.memory.engine import analyze_memory_episode
from mammal.memory.recall import record_cued_recall
from mammal.models.entities import Trial, TrialEvent
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController


def test_full_memory_encoding_recall_and_analysis_workflow(temp_settings: Settings, session: Session):
    load_and_register_all_protocols(session)

    controller = SessionController(session)
    participant = controller.get_or_create_participant("Memory Subject")
    episode = controller.start_session(
        protocol_id="p02_cued_recall_jol",
        participant_id=participant.id,
        item_limit=4,
    )
    episode_id = episode.id

    pairs = [
        ("adui", "enemy", 90.0, "enemy"),      # High JOL, Correct
        ("chakula", "food", 80.0, "food"),      # High JOL, Correct
        ("mwezi", "moon", 30.0, "Wrong"),       # Low JOL, Incorrect
        ("safari", "journey", 20.0, "missing"), # Low JOL, Missing
    ]

    trials = session.query(Trial).filter(Trial.episode_id == episode_id).order_by(Trial.trial_index.asc()).all()

    # 1. Encoding Phase: Record JOL forecasts
    for i, (cue, target, jol, _) in enumerate(pairs):
        t_id = trials[i].id
        item_id = f"pair_swahili_{i}"
        record_encoding_jol(
            session=session,
            trial_id=t_id,
            episode_id=episode_id,
            item_id=item_id,
            cue=cue,
            target=target,
            study_duration_ms=4000.0,
            jol_rating=jol,
            jol_latency_ms=800.0,
        )

    # 2. Recall Phase: Record cued recall responses
    for i, (cue, target, _, ans) in enumerate(pairs):
        t_id = trials[i].id
        item_id = f"pair_swahili_{i}"
        record_cued_recall(
            session=session,
            recall_trial_id=t_id,
            encoding_trial_id=t_id,
            episode_id=episode_id,
            item_id=item_id,
            cue=cue,
            target=target,
            provided_answer=ans,
            response_latency_ms=1200.0,
        )

    # 3. Analyze Programmatically
    res = analyze_memory_episode(session, episode_id, app_settings=temp_settings)
    analysis = res["analysis"]
    assert analysis.total_pairs == 4
    assert analysis.recall_accuracy == 0.50
    assert analysis.gamma_correlation == 1.0  # Perfect prospective discrimination
    assert analysis.prospective_auroc == 1.0

    # 4. Verify artifact store
    store = ArtifactStore(temp_settings)
    art = res["artifact"]
    content = store.read_artifact_bytes(session, art.artifact_id)
    assert b"gamma_correlation" in content

    runner = CliRunner()

    # 5. Test CLI memory-analyze
    res_cli = runner.invoke(
        main,
        ["memory-analyze", episode_id],
        env={"MAMMAL_DATA_ROOT": str(temp_settings.data_root)},
    )
    assert res_cli.exit_code == 0
    assert "MAMMAL Future-Memory & JOL Metacognition" in res_cli.output
    assert "Goodman-Kruskal Gamma" in res_cli.output
    assert "+1.0000" in res_cli.output
