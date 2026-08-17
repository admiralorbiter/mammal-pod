"""Web routes and API endpoints for Project MAMMAL session runner."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, current_app, jsonify, redirect, render_template, request, url_for
from sqlalchemy import func, select

from mammal.capture.voice_pipeline import (
    process_voice_trial_response,
    record_transcription_correction,
)
from mammal.config import Settings, settings
from mammal.db import get_session
from mammal.events.engine import InvariantViolationError
from mammal.models.entities import Episode, Protocol, Trial
from mammal.processors.asr import get_asr_adapter
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.controller import SessionController

routes = Blueprint("routes", __name__)


def _current_settings() -> Settings:
    """Resolve active application settings from Flask config or global default."""
    try:
        return current_app.config.get("SETTINGS") or settings
    except RuntimeError:
        return settings


@routes.route("/")
def index():
    """Render dashboard and session launcher."""
    app_set = _current_settings()
    with get_session(app_set) as session:
        protocols = load_and_register_all_protocols(session)
        if not protocols:
            protocols = list(session.scalars(select(Protocol)).all())
        return render_template("index.html", protocols=protocols)


@routes.route("/sessions/start", methods=["POST"])
def start_session():
    """Start a new experiment session episode."""
    protocol_id = request.form.get("protocol_id", "e00_instrument_qualification")
    pseudonym = request.form.get("pseudonym", "Jonathan Lane")
    app_set = _current_settings()

    with get_session(app_set) as session:
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
    app_set = _current_settings()
    with get_session(app_set) as session:
        controller = SessionController(session)
        trial = controller.get_active_trial(episode_id)
        if trial:
            return redirect(url_for("routes.trial_view", episode_id=episode_id, trial_id=trial.id))
        return redirect(url_for("routes.session_summary", episode_id=episode_id))


@routes.route("/sessions/<episode_id>/trials/<trial_id>")
def trial_view(episode_id: str, trial_id: str):
    """Render individual trial screen and record prompt presentation."""
    app_set = _current_settings()
    with get_session(app_set) as session:
        controller = SessionController(session)
        trial = session.get(Trial, trial_id)
        if not trial or trial.episode_id != episode_id:
            return redirect(url_for("routes.index"))

        episode = session.get(Episode, episode_id)
        protocol = (
            session.query(Protocol)
            .filter(
                Protocol.protocol_id == episode.protocol_id,
                Protocol.version == episode.protocol_version,
            )
            .first()
            if episode
            else None
        )
        conf_cfg = (protocol.schema_json.get("confidence") or {}) if protocol and protocol.schema_json else {}
        conf_enabled = conf_cfg.get("enabled", True)

        item = controller.get_trial_item(trial)
        total_trials = session.query(func.count(Trial.id)).filter(Trial.episode_id == episode_id).scalar() or 0

        # Mark prompt shown event
        controller.mark_prompt_shown(trial_id)

        template_name = "rdk_stimulus.html" if protocol and protocol.domain in ("perception_rdk", "perceptual_psychophysics") else "trial.html"

        return render_template(
            template_name,
            trial=trial,
            episode=episode,
            item=item,
            protocol=protocol,
            total_trials=total_trials,
            confidence_enabled=conf_enabled,
            confidence_config=conf_cfg,
        )


@routes.route("/qualification/display")
def display_qualification():
    """Render P00 display timing and refresh rate qualification page."""
    return render_template("display_qualification.html")


@routes.route("/api/qualification/display", methods=["POST"])
def api_qualify_display():
    """API endpoint to audit client display refresh rate, jitter, and dropped frames."""
    from dataclasses import asdict
    from mammal.psychophysics.display import qualify_display

    data = request.get_json(silent=True) or {}
    intervals = data.get("frame_intervals_ms", [])
    width = int(data.get("viewport_width", 1920))
    height = int(data.get("viewport_height", 1080))
    dpr = float(data.get("device_pixel_ratio", 1.0))
    fullscreen = bool(data.get("fullscreen", False))

    res = qualify_display(
        frame_intervals_ms=intervals,
        viewport_width=width,
        viewport_height=height,
        device_pixel_ratio=dpr,
        fullscreen=fullscreen,
    )
    return jsonify(asdict(res))


@routes.route("/api/trials/<trial_id>/stimulus/start", methods=["POST"])
def api_stimulus_start(trial_id: str):
    """Log stimulus.started event for high-precision perceptual onset timing."""
    from mammal.events.engine import EventEngine

    try:
        app_set = _current_settings()
        with get_session(app_set) as session:
            trial = session.get(Trial, trial_id)
            if trial:
                engine = EventEngine(session)
                engine.record_event(
                    trial_id=trial.id,
                    episode_id=trial.episode_id,
                    event_type="stimulus.started",
                    actor="client",
                    payload={"client_time_ms": (request.get_json(silent=True) or {}).get("client_time_ms")},
                )
                session.commit()
            return jsonify({"status": "started", "trial_id": trial_id})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@routes.route("/api/trials/<trial_id>/answer", methods=["POST"])
def api_lock_answer(trial_id: str):
    """API endpoint to lock participant answer."""
    data = request.get_json(silent=True) or {}
    value = data.get("value")
    modality = data.get("modality", "button")
    latency_ms = data.get("latency_ms")
    raw_artifact_id = data.get("raw_artifact_id")
    frame_intervals = data.get("frame_intervals_ms")

    if value is None:
        return jsonify({"error": "Missing answer value"}), 400

    try:
        app_set = _current_settings()
        with get_session(app_set) as session:
            # If client provided frame timing telemetry, log stimulus.frame_timing event
            if frame_intervals:
                from mammal.events.engine import EventEngine
                import numpy as np
                trial = session.get(Trial, trial_id)
                if trial:
                    engine = EventEngine(session)
                    median_frame = float(np.median(frame_intervals)) if frame_intervals else 16.67
                    engine.record_event(
                        trial_id=trial.id,
                        episode_id=trial.episode_id,
                        event_type="stimulus.ended",
                        actor="client",
                        payload={
                            "frame_count": len(frame_intervals),
                            "median_frame_interval_ms": round(median_frame, 2),
                            "estimated_fps": round(1000.0 / median_frame, 1) if median_frame > 0 else 60.0,
                        },
                    )

            controller = SessionController(session)
            answer = controller.lock_answer(
                trial_id=trial_id,
                value=value,
                modality=modality,
                latency_ms=float(latency_ms) if latency_ms is not None else None,
                raw_artifact_id=raw_artifact_id,
            )
            trial = session.get(Trial, trial_id)
            return jsonify({
                "status": "locked",
                "trial_id": trial_id,
                "answer_id": answer.id,
                "value": answer.locked_value_json,
                "trial_status": trial.status if trial else "answer_locked",
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

        app_set = _current_settings()
        with get_session(app_set) as session:
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


@routes.route("/qualification/microphone")
def microphone_qualification():
    """Render microphone hardware test and level qualification interface."""
    return render_template("microphone_qualification.html")


@routes.route("/api/trials/<trial_id>/audio/upload", methods=["POST"])
def api_upload_audio(trial_id: str):
    """API endpoint to upload spoken answer audio and trigger transcription."""
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided in multipart request."}), 400

    audio_file = request.files["audio"]
    audio_bytes = audio_file.read()
    mime_type = audio_file.content_type or "audio/webm"
    duration_ms = request.form.get("duration_ms")

    if not audio_bytes:
        return jsonify({"error": "Uploaded audio payload is empty."}), 400

    try:
        custom_adapter = current_app.config.get("ASR_ADAPTER")
        if custom_adapter:
            adapter = custom_adapter
        elif current_app.config.get("TESTING"):
            adapter = get_asr_adapter("mock")
        else:
            try:
                adapter = get_asr_adapter("faster-whisper")
            except Exception:
                adapter = get_asr_adapter("mock")

        app_set = _current_settings()
        with get_session(app_set) as session:
            result = process_voice_trial_response(
                session=session,
                trial_id=trial_id,
                audio_bytes=audio_bytes,
                mime_type=mime_type,
                asr_adapter=adapter,
                app_settings=app_set,
                duration_ms=float(duration_ms) if duration_ms else None,
            )
            return jsonify(result), 200 if result.get("status") == "transcribed" else 500

    except Exception as exc:
        return jsonify({"error": f"Failed to process voice capture: {exc}"}), 500


@routes.route("/api/trials/<trial_id>/transcription/correct", methods=["POST"])
def api_correct_transcription(trial_id: str):
    """API endpoint to record an append-only transcription correction event."""
    data = request.get_json(silent=True) or {}
    corrected_text = data.get("corrected_text")
    reason = data.get("reason", "participant_correction")

    if not corrected_text:
        return jsonify({"error": "Missing corrected_text."}), 400

    try:
        app_set = _current_settings()
        with get_session(app_set) as session:
            record_transcription_correction(
                session=session,
                trial_id=trial_id,
                corrected_text=corrected_text,
                reason=reason,
            )
            return jsonify({"status": "corrected", "trial_id": trial_id})
    except Exception as exc:
        return jsonify({"error": f"Failed to record correction: {exc}"}), 500


@routes.route("/sessions/<episode_id>/summary")
def session_summary(episode_id: str):
    """Render neutral completion summary without revealing scores."""
    app_set = _current_settings()
    with get_session(app_set) as session:
        episode = session.get(Episode, episode_id)
        if not episode:
            return redirect(url_for("routes.index"))

        total_trials = session.query(func.count(Trial.id)).filter(Trial.episode_id == episode_id).scalar() or 0
        return render_template("summary.html", episode=episode, total_trials=total_trials)

