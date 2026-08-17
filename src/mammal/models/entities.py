"""Relational domain models for Project MAMMAL provenance kernel."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mammal.db import Base
from mammal.models.base import JSONEncodedDict, UTCDateTime, generate_uuid, utc_now


class Participant(Base):
    """Participant entity (Big Boss living original record)."""

    __tablename__ = "participants"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_uuid)
    pseudonym: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    consent_record_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)

    episodes: Mapped[list[Episode]] = relationship("Episode", back_populates="participant")


class Experiment(Base):
    """Experiment registration entity."""

    __tablename__ = "experiments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    research_question: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="engineering", nullable=False)
    protocol_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    analysis_plan_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ethics_determination: Mapped[str | None] = mapped_column(String(128), nullable=True)
    preregistration_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    code_commit: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)

    episodes: Mapped[list[Episode]] = relationship("Episode", back_populates="experiment")


class Protocol(Base):
    """Protocol version registration entity."""

    __tablename__ = "protocols"

    protocol_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    version: Mapped[str] = mapped_column(String(32), primary_key=True)
    domain: Mapped[str] = mapped_column(String(64), nullable=False)
    mode: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="engineering", nullable=False)
    schema_json: Mapped[dict[str, Any]] = mapped_column(JSONEncodedDict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)


class Item(Base):
    """Item bank entry."""

    __tablename__ = "items"

    item_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    version: Mapped[str] = mapped_column(String(32), primary_key=True)
    domain: Mapped[str] = mapped_column(String(64), nullable=False)
    family: Mapped[str] = mapped_column(String(64), nullable=False)
    prompt_json: Mapped[dict[str, Any] | str] = mapped_column(JSONEncodedDict, nullable=False)
    options_json: Mapped[list[Any] | None] = mapped_column(JSONEncodedDict, nullable=True)
    ground_truth_json: Mapped[Any] = mapped_column(JSONEncodedDict, nullable=False)
    partition: Mapped[str] = mapped_column(String(32), nullable=False)
    source_json: Mapped[dict[str, Any]] = mapped_column(JSONEncodedDict, nullable=False)
    difficulty_json: Mapped[dict[str, Any] | None] = mapped_column(JSONEncodedDict, nullable=True)
    verification_json: Mapped[dict[str, Any] | None] = mapped_column(JSONEncodedDict, nullable=True)
    leakage_checks_json: Mapped[list[str] | None] = mapped_column(JSONEncodedDict, nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)


class Episode(Base):
    """Participant session / research episode."""

    __tablename__ = "episodes"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_uuid)
    participant_id: Mapped[str] = mapped_column(String(64), ForeignKey("participants.id"), nullable=False)
    experiment_id: Mapped[str] = mapped_column(String(64), ForeignKey("experiments.id"), nullable=False)
    protocol_id: Mapped[str] = mapped_column(String(64), nullable=False)
    protocol_version: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(32), nullable=False)
    started_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(UTCDateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    environment_json: Mapped[dict[str, Any] | None] = mapped_column(JSONEncodedDict, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    participant: Mapped[Participant] = relationship("Participant", back_populates="episodes")
    experiment: Mapped[Experiment] = relationship("Experiment", back_populates="episodes")
    trials: Mapped[list[Trial]] = relationship("Trial", back_populates="episode", cascade="all, delete-orphan")


class Trial(Base):
    """Single first-order cognitive trial."""

    __tablename__ = "trials"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_uuid)
    episode_id: Mapped[str] = mapped_column(String(64), ForeignKey("episodes.id"), nullable=False)
    item_id: Mapped[str] = mapped_column(String(64), nullable=False)
    item_version: Mapped[str] = mapped_column(String(32), nullable=False)
    trial_index: Mapped[int] = mapped_column(Integer, nullable=False)
    condition: Mapped[str | None] = mapped_column(String(64), nullable=True)
    randomization_seed: Mapped[str | None] = mapped_column(String(64), nullable=True)
    option_order_json: Mapped[list[Any] | None] = mapped_column(JSONEncodedDict, nullable=True)
    prompt_shown_at: Mapped[datetime | None] = mapped_column(UTCDateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(UTCDateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="created", nullable=False)

    episode: Mapped[Episode] = relationship("Episode", back_populates="trials")
    answer: Mapped[Answer | None] = relationship("Answer", back_populates="trial", uselist=False)
    confidence: Mapped[Confidence | None] = relationship("Confidence", back_populates="trial", uselist=False)
    outcome: Mapped[Outcome | None] = relationship("Outcome", back_populates="trial", uselist=False)
    events: Mapped[list[TrialEvent]] = relationship("TrialEvent", back_populates="trial", order_by="TrialEvent.occurred_at")

    __table_args__ = (
        Index("ix_trials_episode_index", "episode_id", "trial_index", unique=True),
    )


class Artifact(Base):
    """Immutable binary or derived artifact record."""

    __tablename__ = "artifacts"

    artifact_id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_uuid)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    mime_type: Mapped[str] = mapped_column(String(128), nullable=False)
    rel_path: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    byte_count: Mapped[int] = mapped_column(Integer, nullable=False)
    source_artifact_ids_json: Mapped[list[str] | None] = mapped_column(JSONEncodedDict, nullable=True)
    processor_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    retention_class: Mapped[str] = mapped_column(String(32), default="raw", nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)


class Answer(Base):
    """Locked canonical participant response."""

    __tablename__ = "answers"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_uuid)
    trial_id: Mapped[str] = mapped_column(String(64), ForeignKey("trials.id"), unique=True, nullable=False)
    modality: Mapped[str] = mapped_column(String(32), nullable=False)
    locked_value_json: Mapped[Any] = mapped_column(JSONEncodedDict, nullable=False)
    locked_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)
    raw_artifact_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("artifacts.artifact_id"), nullable=True)
    transcript_artifact_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("artifacts.artifact_id"), nullable=True)
    response_latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    parser_version: Mapped[str | None] = mapped_column(String(64), nullable=True)

    trial: Mapped[Trial] = relationship("Trial", back_populates="answer")


class Confidence(Base):
    """Participant explicit confidence rating."""

    __tablename__ = "confidence_ratings"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_uuid)
    trial_id: Mapped[str] = mapped_column(String(64), ForeignKey("trials.id"), unique=True, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    modality: Mapped[str] = mapped_column(String(32), nullable=False)
    scale_min: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    scale_max: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    locked_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)
    raw_artifact_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("artifacts.artifact_id"), nullable=True)
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)

    trial: Mapped[Trial] = relationship("Trial", back_populates="confidence")

    __table_args__ = (
        CheckConstraint("value >= scale_min AND value <= scale_max", name="check_confidence_range"),
    )


class Outcome(Base):
    """Canonical correctness outcome."""

    __tablename__ = "outcomes"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_uuid)
    trial_id: Mapped[str] = mapped_column(String(64), ForeignKey("trials.id"), unique=True, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    scoring_rule: Mapped[str] = mapped_column(String(64), nullable=False)
    scorer_provenance: Mapped[str] = mapped_column(String(128), nullable=False)
    scored_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)

    trial: Mapped[Trial] = relationship("Trial", back_populates="outcome")


class TrialEvent(Base):
    """Append-only trial event with cryptographic chain hash."""

    __tablename__ = "trial_events"

    event_id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_uuid)
    trial_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("trials.id"), nullable=True)
    episode_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("episodes.id"), nullable=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    occurred_at: Mapped[datetime] = mapped_column(UTCDateTime, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)
    actor: Mapped[str] = mapped_column(String(32), nullable=False)
    schema_version: Mapped[str] = mapped_column(String(32), default="1.0.0", nullable=False)
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSONEncodedDict, nullable=False)
    previous_event_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    event_hash: Mapped[str] = mapped_column(String(64), nullable=False)

    trial: Mapped[Trial | None] = relationship("Trial", back_populates="events")

    __table_args__ = (
        Index("ix_events_trial_occurred", "trial_id", "occurred_at"),
        Index("ix_events_episode_occurred", "episode_id", "occurred_at"),
    )


class ObserverRun(Base):
    """Execution run of an external model observer."""

    __tablename__ = "observer_runs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_uuid)
    observer_id: Mapped[str] = mapped_column(String(64), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    model_name: Mapped[str] = mapped_column(String(128), nullable=False)
    visibility_contract_id: Mapped[str] = mapped_column(String(64), nullable=False)
    history_cutoff_at: Mapped[datetime | None] = mapped_column(UTCDateTime, nullable=True)
    prompt_compiler_version: Mapped[str] = mapped_column(String(64), nullable=False)
    started_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(UTCDateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="started", nullable=False)

    predictions: Mapped[list[ObserverPrediction]] = relationship("ObserverPrediction", back_populates="observer_run")


class ObserverPrediction(Base):
    """Prediction generated by an observer for a specific trial."""

    __tablename__ = "observer_predictions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_uuid)
    observer_run_id: Mapped[str] = mapped_column(String(64), ForeignKey("observer_runs.id"), nullable=False)
    trial_id: Mapped[str] = mapped_column(String(64), ForeignKey("trials.id"), nullable=False)
    p_correct: Mapped[float] = mapped_column(Float, nullable=False)
    compliance: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    raw_output_json: Mapped[dict[str, Any] | None] = mapped_column(JSONEncodedDict, nullable=True)
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)

    observer_run: Mapped[ObserverRun] = relationship("ObserverRun", back_populates="predictions")


class ClaimRecord(Base):
    """Accepted scientific claim ledger entry."""

    __tablename__ = "claim_records"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    conventional_wording: Mapped[str] = mapped_column(Text, nullable=False)
    metal_gear_shorthand: Mapped[str | None] = mapped_column(String(256), nullable=True)
    evidence_manifest_json: Mapped[list[str]] = mapped_column(JSONEncodedDict, nullable=False)
    domain: Mapped[str] = mapped_column(String(64), nullable=False)
    epistemic_status: Mapped[str] = mapped_column(String(32), nullable=False)
    ratified_by_participant: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)
    superseded_by: Mapped[str | None] = mapped_column(String(64), nullable=True)


class DecisionRecord(Base):
    """Explicit governance and architectural decision record."""

    __tablename__ = "decision_records"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    context: Mapped[str] = mapped_column(Text, nullable=False)
    decision: Mapped[str] = mapped_column(Text, nullable=False)
    reconsideration_trigger: Mapped[str | None] = mapped_column(Text, nullable=True)
    decided_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)


class DeviationRecord(Base):
    """Protocol deviation and anomaly tracking."""

    __tablename__ = "deviation_records"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_uuid)
    protocol_id: Mapped[str] = mapped_column(String(64), nullable=False)
    episode_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    trial_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    impact_assessment: Mapped[str] = mapped_column(Text, nullable=False)
    remedy_action: Mapped[str] = mapped_column(Text, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now, nullable=False)
