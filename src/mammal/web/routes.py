"""Web routes and API endpoints for Project MAMMAL session runner."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from sqlalchemy import func, select

from mammal.db import get_session
from mammal.events.engine import InvariantViolationError
from mammal.models.entities import Episode, Protocol, Trial
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController

routes = Blueprint("routes", __name__)


@routes.route("/")
def index():
    """Render dashboard and session launcher."""
    with get_session() as session:
        protocols = load_and_register_all_protocols(session)
        if not protocols:
            protocols = list(session.scalars(select(Protocol)).all())
        return render_template("index.html", protocols=protocols)


@routes.route("/sessions/start", methods=["POST"])
def start_session():
    """Start a new experiment session episode."""
    protocol_id = request.form.get("protocol_id", "e00_instrument_qualification")
    pseudonym = request.form.get("pseudonym", "Jonathan Lane")

    with get_session() as session:
        controller = SessionController(session)
        participant = controller.get_or_create_participant(pseudonym=pseudonym)
        episode = controller.start_session(
            protocol_id=protocol_id,
            participant_id=participant.id,
        )
        episode_id = episode.id

    return redirect(url_for("routes.session_view", episode_id=episode_id))


@routes.route("/sessions/<episode_id>")
def session_view(episode_id: str):
    """Direct participant to current active trial or completion summary."""
    with get_session() as session:
        controller = SessionController(session)
        trial = controller.get_active_trial(episode_id)
        if trial:
            return redirect(url_for("routes.trial_view", episode_id=episode_id, trial_id=trial.id))
        return redirect(url_for("routes.session_summary", episode_id=episode_id))


@routes.route("/sessions/<episode_id>/trials/<trial_id>")
def trial_view(episode_id: str, trial_id: str):
    """Render individual trial screen and record prompt presentation."""
    with get_session() as session:
        controller = SessionController(session)
        trial = session.get(Trial, trial_id)
        if not trial or trial.episode_id != episode_id:
            return redirect(url_for("routes.index"))

        episode = session.get(Episode, episode_id)
        item = controller.get_trial_item(trial)
        total_trials = session.query(func.count(Trial.id)).filter(Trial.episode_id == episode_id).scalar() or 0

        # Mark prompt shown event
        controller.mark_prompt_shown(trial_id)

        return render_template(
            "trial.html",
            trial=trial,
            episode=episode,
            item=item,
            total_trials=total_trials,
        )


@routes.route("/api/trials/<trial_id>/answer", methods=["POST"])
def api_lock_answer(trial_id: str):
    """API endpoint to lock participant answer."""
    data = request.get_json(silent=True) or {}
    value = data.get("value")
    modality = data.get("modality", "button")
    latency_ms = data.get("latency_ms")

    if value is None:
        return jsonify({"error": "Missing answer value"}), 400

    try:
        with get_session() as session:
            controller = SessionController(session)
            answer = controller.lock_answer(
                trial_id=trial_id,
                value=value,
                modality=modality,
                latency_ms=float(latency_ms) if latency_ms is not None else None,
            )
            return jsonify({
                "status": "locked",
                "trial_id": trial_id,
                "answer_id": answer.id,
                "value": answer.locked_value_json,
            })
    except InvariantViolationError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"Internal server error: {exc}"}), 500


@routes.route("/api/trials/<trial_id>/confidence", methods=["POST"])
def api_lock_confidence(trial_id: str):
    """API endpoint to lock confidence rating and trigger scoring."""
    data = request.get_json(silent=True) or {}
    value = data.get("value")
    modality = data.get("modality", "numeric")
    latency_ms = data.get("latency_ms")

    if value is None:
        return jsonify({"error": "Missing confidence value"}), 400

    try:
        val_float = float(value)
        if not (0.0 <= val_float <= 100.0):
            return jsonify({"error": "Confidence must be between 0.0 and 100.0"}), 400

        with get_session() as session:
            controller = SessionController(session)
            confidence, _ = controller.lock_confidence(
                trial_id=trial_id,
                value=val_float,
                modality=modality,
                latency_ms=float(latency_ms) if latency_ms is not None else None,
            )
            return jsonify({
                "status": "completed",
                "trial_id": trial_id,
                "confidence": confidence.value,
            })
    except InvariantViolationError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"Internal server error: {exc}"}), 500


@routes.route("/sessions/<episode_id>/summary")
def session_summary(episode_id: str):
    """Render neutral completion summary without revealing scores."""
    with get_session() as session:
        episode = session.get(Episode, episode_id)
        if not episode:
            return redirect(url_for("routes.index"))

        total_trials = session.query(func.count(Trial.id)).filter(Trial.episode_id == episode_id).scalar() or 0
        return render_template("summary.html", episode=episode, total_trials=total_trials)
