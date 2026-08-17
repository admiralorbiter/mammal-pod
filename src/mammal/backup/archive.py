"""Cold backup export and archive restoration for Project MAMMAL sessions."""

from __future__ import annotations

from datetime import datetime
import json
import tarfile
import tempfile
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from mammal.artifacts.store import ArtifactStore, compute_sha256
from mammal.config import Settings
from mammal.db import create_db_engine, get_session, init_db
from mammal.events.engine import canonical_json_dumps
from mammal.models.base import utc_now
from mammal.models.entities import (
    Answer,
    Artifact,
    Confidence,
    Episode,
    Experiment,
    Outcome,
    Participant,
    Protocol,
    Trial,
    TrialEvent,
)


def export_session_archive(
    session: Session,
    episode_id: str,
    output_path: str | Path,
    app_settings: Settings | None = None,
) -> Path:
    """Export complete episode bundle (metadata, events, DB state, and raw/derived artifacts) into a portable .tar.gz archive."""
    episode = session.get(Episode, episode_id)
    if not episode:
        raise ValueError(f"Episode {episode_id} not found.")

    trials = session.query(Trial).filter(Trial.episode_id == episode_id).all()
    trial_ids = [t.id for t in trials]

    events = (
        session.query(TrialEvent)
        .filter(TrialEvent.episode_id == episode_id)
        .order_by(TrialEvent.occurred_at.asc())
        .all()
    )

    participant = session.get(Participant, episode.participant_id) if episode.participant_id else None
    protocol = (
        session.query(Protocol)
        .filter(Protocol.protocol_id == episode.protocol_id, Protocol.version == episode.protocol_version)
        .first()
    )
    experiment = session.get(Experiment, episode.experiment_id) if episode.experiment_id else None

    # Collect answers, confidences, outcomes
    answers = session.query(Answer).filter(Answer.trial_id.in_(trial_ids)).all() if trial_ids else []
    confidences = session.query(Confidence).filter(Confidence.trial_id.in_(trial_ids)).all() if trial_ids else []
    outcomes = session.query(Outcome).filter(Outcome.trial_id.in_(trial_ids)).all() if trial_ids else []

    # Collect artifacts referenced by trials/answers/events
    artifact_ids = set()
    for ans in answers:
        if ans.raw_artifact_id:
            artifact_ids.add(ans.raw_artifact_id)
    for ev in events:
        p = ev.payload_json or {}
        if p.get("raw_artifact_id"):
            artifact_ids.add(p["raw_artifact_id"])
        if p.get("artifact_id"):
            artifact_ids.add(p["artifact_id"])

    artifacts = session.query(Artifact).filter(Artifact.artifact_id.in_(artifact_ids)).all() if artifact_ids else []

    store = ArtifactStore(app_settings)
    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Build bundle data dictionary
        bundle_data: dict[str, Any] = {
            "version": "1.0",
            "episode": {
                "id": episode.id,
                "participant_id": episode.participant_id,
                "experiment_id": episode.experiment_id,
                "protocol_id": episode.protocol_id,
                "protocol_version": episode.protocol_version,
                "mode": episode.mode,
                "status": episode.status,
                "started_at": episode.started_at.isoformat() if episode.started_at else None,
                "ended_at": episode.ended_at.isoformat() if episode.ended_at else None,
            },
            "participant": {
                "id": participant.id,
                "pseudonym": participant.pseudonym,
                "created_at": participant.created_at.isoformat() if participant and participant.created_at else None,
            } if participant else None,
            "protocol": {
                "protocol_id": protocol.protocol_id,
                "version": protocol.version,
                "domain": protocol.domain,
                "mode": protocol.mode,
                "schema_json": protocol.schema_json,
            } if protocol else None,
            "experiment": {
                "id": experiment.id,
                "title": experiment.title,
                "research_question": experiment.research_question,
            } if experiment else None,
            "trials": [
                {
                    "id": t.id,
                    "item_id": t.item_id,
                    "item_version": t.item_version,
                    "trial_index": t.trial_index,
                    "status": t.status,
                }
                for t in trials
            ],
            "answers": [
                {
                    "id": a.id,
                    "trial_id": a.trial_id,
                    "modality": a.modality,
                    "locked_value_json": a.locked_value_json,
                    "locked_at": a.locked_at.isoformat() if a.locked_at else None,
                    "raw_artifact_id": a.raw_artifact_id,
                    "response_latency_ms": a.response_latency_ms,
                }
                for a in answers
            ],
            "confidences": [
                {
                    "id": c.id,
                    "trial_id": c.trial_id,
                    "value": c.value,
                    "modality": c.modality,
                    "scale_min": c.scale_min,
                    "scale_max": c.scale_max,
                    "locked_at": c.locked_at.isoformat() if c.locked_at else None,
                    "latency_ms": c.latency_ms,
                }
                for c in confidences
            ],
            "outcomes": [
                {
                    "id": o.id,
                    "trial_id": o.trial_id,
                    "score": o.score,
                    "is_correct": o.is_correct,
                    "scoring_rule": o.scoring_rule,
                    "scorer_provenance": o.scorer_provenance,
                    "scored_at": o.scored_at.isoformat() if o.scored_at else None,
                }
                for o in outcomes
            ],
            "events": [
                {
                    "event_id": e.event_id,
                    "episode_id": e.episode_id,
                    "trial_id": e.trial_id,
                    "event_type": e.event_type,
                    "occurred_at": e.occurred_at.isoformat() if e.occurred_at else None,
                    "actor": e.actor,
                    "schema_version": e.schema_version,
                    "payload_json": e.payload_json,
                    "previous_event_hash": e.previous_event_hash,
                    "event_hash": e.event_hash,
                }
                for e in events
            ],
            "artifacts": [
                {
                    "artifact_id": art.artifact_id,
                    "rel_path": art.rel_path,
                    "sha256": art.sha256,
                    "byte_count": art.byte_count,
                    "mime_type": art.mime_type,
                    "retention_class": art.retention_class,
                    "source_artifact_ids_json": art.source_artifact_ids_json,
                    "processor_version": art.processor_version,
                }
                for art in artifacts
            ],
        }

        # Write manifest.json
        manifest_file = tmp_path / "bundle.json"
        manifest_file.write_text(json.dumps(bundle_data, indent=2), encoding="utf-8")

        # Copy physical artifact files
        artifacts_dir = tmp_path / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        for art in artifacts:
            src_path = store._resolve_path(art.rel_path)
            if src_path.exists():
                dst_path = artifacts_dir / art.rel_path
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                dst_path.write_bytes(src_path.read_bytes())

        # Create tar.gz archive
        with tarfile.open(out_file, "w:gz") as tar:
            tar.add(tmp_path / "bundle.json", arcname="bundle.json")
            if artifacts_dir.exists():
                tar.add(artifacts_dir, arcname="artifacts")

    return out_file


def restore_session_archive(
    archive_path: str | Path,
    target_settings: Settings,
) -> str:
    """Restore a session archive into a clean data root, preserving checksums and event integrity."""
    target_settings.ensure_directories()
    engine = create_db_engine(target_settings.db_url)
    init_db(engine)

    arch = Path(archive_path).resolve()
    if not arch.exists():
        raise FileNotFoundError(f"Archive file not found: {arch}")

    store = ArtifactStore(target_settings)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        with tarfile.open(arch, "r:gz") as tar:
            tar.extractall(tmp_path)

        bundle_file = tmp_path / "bundle.json"
        if not bundle_file.exists():
            raise ValueError("Corrupted archive: bundle.json missing.")

        bundle = json.loads(bundle_file.read_text(encoding="utf-8"))

        # 1. Restore physical artifact files
        artifacts_dir = tmp_path / "artifacts"
        if artifacts_dir.exists():
            for fpath in artifacts_dir.rglob("*"):
                if fpath.is_file():
                    rel = fpath.relative_to(artifacts_dir)
                    target_dst = store._resolve_path(str(rel))
                    target_dst.parent.mkdir(parents=True, exist_ok=True)
                    target_dst.write_bytes(fpath.read_bytes())

        # 2. Restore database records
        from mammal.items.bank import seed_qualification_items
        with get_session(target_settings) as session:
            seed_qualification_items(session)
            session.flush()

            # Restore participant
            p_data = bundle.get("participant")
            if p_data:
                existing_p = session.get(Participant, p_data["id"])
                if not existing_p:
                    p = Participant(
                        id=p_data["id"],
                        pseudonym=p_data["pseudonym"],
                    )
                    session.add(p)

            # Restore protocol
            pr_data = bundle.get("protocol")
            if pr_data:
                existing_pr = (
                    session.query(Protocol)
                    .filter(Protocol.protocol_id == pr_data["protocol_id"], Protocol.version == pr_data["version"])
                    .first()
                )
                if not existing_pr:
                    pr = Protocol(
                        protocol_id=pr_data["protocol_id"],
                        version=pr_data["version"],
                        domain=pr_data["domain"],
                        mode=pr_data["mode"],
                        status="engineering",
                        schema_json=pr_data["schema_json"],
                    )
                    session.add(pr)

            # Restore experiment
            exp_data = bundle.get("experiment")
            if exp_data:
                existing_exp = session.get(Experiment, exp_data["id"])
                if not existing_exp:
                    exp = Experiment(
                        id=exp_data["id"],
                        title=exp_data["title"],
                        research_question=exp_data["research_question"],
                    )
                    session.add(exp)

            session.flush()

            # Restore episode
            ep_data = bundle["episode"]
            existing_ep = session.get(Episode, ep_data["id"])
            if not existing_ep:
                ep = Episode(
                    id=ep_data["id"],
                    participant_id=ep_data["participant_id"],
                    experiment_id=ep_data["experiment_id"],
                    protocol_id=ep_data["protocol_id"],
                    protocol_version=ep_data["protocol_version"],
                    mode=ep_data["mode"],
                    status=ep_data["status"],
                )
                session.add(ep)

            session.flush()

            # Restore artifacts metadata BEFORE answers and events
            for art_data in bundle.get("artifacts", []):
                if not session.get(Artifact, art_data["artifact_id"]):
                    art = Artifact(
                        artifact_id=art_data["artifact_id"],
                        rel_path=art_data["rel_path"],
                        sha256=art_data["sha256"],
                        byte_count=art_data["byte_count"],
                        mime_type=art_data["mime_type"],
                        retention_class=art_data["retention_class"],
                        source_artifact_ids_json=art_data.get("source_artifact_ids_json"),
                        processor_version=art_data.get("processor_version"),
                    )
                    session.add(art)

            session.flush()

            # Restore trials
            for t_data in bundle.get("trials", []):
                if not session.get(Trial, t_data["id"]):
                    t = Trial(
                        id=t_data["id"],
                        episode_id=ep_data["id"],
                        item_id=t_data["item_id"],
                        item_version=t_data["item_version"],
                        trial_index=t_data["trial_index"],
                        status=t_data["status"],
                    )
                    session.add(t)

            session.flush()

            # Restore answers
            for a_data in bundle.get("answers", []):
                if not session.get(Answer, a_data["id"]):
                    locked_dt = datetime.fromisoformat(a_data["locked_at"]) if a_data.get("locked_at") else utc_now()
                    ans = Answer(
                        id=a_data["id"],
                        trial_id=a_data["trial_id"],
                        modality=a_data["modality"],
                        locked_value_json=a_data["locked_value_json"],
                        locked_at=locked_dt,
                        raw_artifact_id=a_data.get("raw_artifact_id"),
                        response_latency_ms=a_data.get("response_latency_ms"),
                    )
                    session.add(ans)

            # Restore confidences
            for c_data in bundle.get("confidences", []):
                if not session.get(Confidence, c_data["id"]):
                    locked_c_dt = datetime.fromisoformat(c_data["locked_at"]) if c_data.get("locked_at") else utc_now()
                    conf = Confidence(
                        id=c_data["id"],
                        trial_id=c_data["trial_id"],
                        value=c_data["value"],
                        modality=c_data["modality"],
                        scale_min=c_data.get("scale_min", 0.0),
                        scale_max=c_data.get("scale_max", 100.0),
                        locked_at=locked_c_dt,
                        latency_ms=c_data.get("latency_ms"),
                    )
                    session.add(conf)

            # Restore outcomes
            for o_data in bundle.get("outcomes", []):
                if not session.get(Outcome, o_data["id"]):
                    scored_dt = datetime.fromisoformat(o_data["scored_at"]) if o_data.get("scored_at") else utc_now()
                    out = Outcome(
                        id=o_data["id"],
                        trial_id=o_data["trial_id"],
                        score=o_data["score"],
                        is_correct=o_data["is_correct"],
                        scoring_rule=o_data["scoring_rule"],
                        scorer_provenance=o_data["scorer_provenance"],
                        scored_at=scored_dt,
                    )
                    session.add(out)

            # Restore events
            for e_data in bundle.get("events", []):
                existing_ev = session.query(TrialEvent).filter(TrialEvent.event_id == e_data["event_id"]).first()
                if not existing_ev:
                    occ_dt = datetime.fromisoformat(e_data["occurred_at"]) if e_data.get("occurred_at") else utc_now()
                    ev = TrialEvent(
                        event_id=e_data["event_id"],
                        episode_id=e_data["episode_id"],
                        trial_id=e_data["trial_id"],
                        event_type=e_data["event_type"],
                        occurred_at=occ_dt,
                        actor=e_data["actor"],
                        schema_version=e_data["schema_version"],
                        payload_json=e_data["payload_json"],
                        previous_event_hash=e_data["previous_event_hash"],
                        event_hash=e_data["event_hash"],
                    )
                    session.add(ev)

            session.commit()

        return ep_data["id"]
