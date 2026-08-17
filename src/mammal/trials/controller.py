"""Trial session controller orchestrating session progression, answer locking, and scoring."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from mammal.events.engine import EventEngine, InvariantViolationError
from mammal.items.bank import get_items_for_protocol
from mammal.models.base import generate_uuid, utc_now
from mammal.models.entities import (
    Answer,
    Confidence,
    Episode,
    Experiment,
    Item,
    Outcome,
    Participant,
    Protocol,
    Trial,
    TrialEvent,
)
from mammal.scoring.engine import score_trial_answer


class SessionController:
    """Orchestrates multi-trial cognitive experiment sessions."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.events = EventEngine(session)

    def get_or_create_participant(self, pseudonym: str = "Jonathan Lane") -> Participant:
        """Fetch or create default participant record."""
        stmt = select(Participant).where(Participant.pseudonym == pseudonym)
        participant = self.session.scalars(stmt).first()
        if not participant:
            participant = Participant(
                id=f"part_{generate_uuid()[:8]}",
                pseudonym=pseudonym,
                status="active",
            )
            self.session.add(participant)
            self.session.flush()
        return participant

    def get_or_create_experiment(
        self,
        experiment_id: str = "e00_inst_qualification",
        title: str = "Instrument Qualification",
        research_question: str = "Can the system preserve a complete trial record?",
    ) -> Experiment:
        """Fetch or create experiment registration."""
        experiment = self.session.get(Experiment, experiment_id)
        if not experiment:
            experiment = Experiment(
                id=experiment_id,
                title=title,
                research_question=research_question,
                status="engineering",
            )
            self.session.add(experiment)
            self.session.flush()
        return experiment

    def start_session(
        self,
        protocol_id: str,
        protocol_version: str = "0.1.0",
        participant_id: str | None = None,
        experiment_id: str = "e00_inst_qualification",
        mode: str = "observation",
        item_ids: Sequence[str] | None = None,
    ) -> Episode:
        """Initialize a new experiment episode with scheduled trials."""
        if participant_id is None:
            participant = self.get_or_create_participant()
            participant_id = participant.id

        self.get_or_create_experiment(experiment_id=experiment_id)

        # Query protocol
        stmt = select(Protocol).where(Protocol.protocol_id == protocol_id, Protocol.version == protocol_version)
        proto = self.session.scalars(stmt).first()
        if not proto:
            # Create placeholder protocol if not already loaded
            proto = Protocol(
                protocol_id=protocol_id,
                version=protocol_version,
                domain="semantic",
                mode=mode,
                status="engineering",
                schema_json={},
            )
            self.session.add(proto)
            self.session.flush()

        episode = Episode(
            id=f"ses_{generate_uuid()[:12]}",
            participant_id=participant_id,
            experiment_id=experiment_id,
            protocol_id=protocol_id,
            protocol_version=protocol_version,
            mode=mode,
            started_at=utc_now(),
            status="active",
        )
        self.session.add(episode)
        self.session.flush()

        # Select items
        if item_ids:
            items = list(self.session.scalars(select(Item).where(Item.item_id.in_(item_ids))).all())
        else:
            partition = proto.schema_json.get("item_bank", {}).get("partition", "engineering")
            items = list(get_items_for_protocol(self.session, partition=partition, limit=10))

        # Schedule trials
        for idx, item in enumerate(items, start=1):
            trial = Trial(
                id=f"trl_{generate_uuid()[:12]}",
                episode_id=episode.id,
                item_id=item.item_id,
                item_version=item.version,
                trial_index=idx,
                status="created",
            )
            self.session.add(trial)
            self.session.flush()

            self.events.record_event(
                event_type="trial.created",
                actor="server",
                payload={"item_id": item.item_id, "trial_index": idx},
                trial_id=trial.id,
                episode_id=episode.id,
            )

        self.session.commit()
        return episode

    def get_episode(self, episode_id: str) -> Episode | None:
        """Fetch episode by ID."""
        return self.session.get(Episode, episode_id)

    def get_active_trial(self, episode_id: str) -> Trial | None:
        """Get the current uncompleted trial in the episode."""
        stmt = (
            select(Trial)
            .where(Trial.episode_id == episode_id, Trial.status != "completed")
            .order_by(Trial.trial_index.asc())
        )
        return self.session.scalars(stmt).first()

    def get_trial_item(self, trial: Trial) -> Item | None:
        """Fetch the item definition for a trial."""
        stmt = select(Item).where(Item.item_id == trial.item_id, Item.version == trial.item_version)
        return self.session.scalars(stmt).first()

    def mark_prompt_shown(self, trial_id: str) -> None:
        """Record prompt display event if not already recorded."""
        trial = self.session.get(Trial, trial_id)
        if not trial:
            raise ValueError(f"Trial {trial_id} not found.")

        if trial.prompt_shown_at is None:
            trial.prompt_shown_at = utc_now()
            trial.status = "in_progress"
            self.events.record_event(
                event_type="prompt.shown",
                actor="browser",
                payload={"trial_id": trial_id},
                trial_id=trial_id,
                episode_id=trial.episode_id,
            )
            self.session.commit()

    def lock_answer(
        self,
        trial_id: str,
        value: Any,
        modality: str = "button",
        latency_ms: float | None = None,
        raw_artifact_id: str | None = None,
    ) -> Answer:
        """Lock participant answer, enforcing immutability."""
        trial = self.session.get(Trial, trial_id)
        if not trial:
            raise ValueError(f"Trial {trial_id} not found.")

        if trial.answer is not None:
            raise InvariantViolationError(f"Trial {trial_id} already has a locked answer.")

        # Record event first to validate invariants and append to chain
        self.events.record_event(
            event_type="answer.locked",
            actor="participant",
            payload={
                "value": value,
                "modality": modality,
                "latency_ms": latency_ms,
                "raw_artifact_id": raw_artifact_id,
            },
            trial_id=trial_id,
            episode_id=trial.episode_id,
        )

        answer = Answer(
            trial_id=trial_id,
            modality=modality,
            locked_value_json=value,
            locked_at=utc_now(),
            raw_artifact_id=raw_artifact_id,
            response_latency_ms=latency_ms,
        )
        self.session.add(answer)
        trial.status = "answer_locked"
        self.session.commit()
        return answer

    def lock_confidence(
        self,
        trial_id: str,
        value: float,
        modality: str = "numeric",
        latency_ms: float | None = None,
    ) -> tuple[Confidence, Outcome]:
        """Lock confidence rating, trigger deterministic scoring, and complete trial."""
        trial = self.session.get(Trial, trial_id)
        if not trial:
            raise ValueError(f"Trial {trial_id} not found.")

        if trial.answer is None:
            raise InvariantViolationError(f"Cannot lock confidence before answer in trial {trial_id}.")

        if trial.confidence is not None:
            raise InvariantViolationError(f"Confidence already locked for trial {trial_id}.")

        if not (0.0 <= value <= 100.0):
            raise ValueError(f"Confidence rating {value} out of range [0.0, 100.0].")

        # 1. Record confidence event & model
        self.events.record_event(
            event_type="confidence.locked",
            actor="participant",
            payload={
                "value": value,
                "modality": modality,
                "latency_ms": latency_ms,
            },
            trial_id=trial_id,
            episode_id=trial.episode_id,
        )

        confidence = Confidence(
            trial_id=trial_id,
            value=value,
            modality=modality,
            scale_min=0.0,
            scale_max=100.0,
            locked_at=utc_now(),
            latency_ms=latency_ms,
        )
        self.session.add(confidence)

        # 2. Score outcome deterministically
        item = self.get_trial_item(trial)
        gt = item.ground_truth_json if item else {}
        score_res = score_trial_answer(trial.answer.locked_value_json, gt)

        self.events.record_event(
            event_type="outcome.scored",
            actor="processor",
            payload={
                "score": score_res.score,
                "is_correct": score_res.is_correct,
                "scoring_rule": score_res.scoring_rule,
                "scorer": score_res.scorer,
            },
            trial_id=trial_id,
            episode_id=trial.episode_id,
        )

        outcome = Outcome(
            trial_id=trial_id,
            score=score_res.score,
            is_correct=score_res.is_correct,
            scoring_rule=score_res.scoring_rule,
            scorer_provenance=score_res.scorer,
            scored_at=utc_now(),
        )
        self.session.add(outcome)

        # 3. Complete trial
        self.events.record_event(
            event_type="trial.completed",
            actor="server",
            payload={"status": "completed"},
            trial_id=trial_id,
            episode_id=trial.episode_id,
        )

        trial.status = "completed"
        trial.completed_at = utc_now()
        self.session.flush()

        # 4. Check if entire episode is finished
        remaining = (
            self.session.query(Trial)
            .filter(Trial.episode_id == trial.episode_id, Trial.status != "completed")
            .count()
        )
        if remaining == 0:
            episode = self.session.get(Episode, trial.episode_id)
            if episode:
                episode.status = "completed"
                episode.ended_at = utc_now()

        self.session.commit()
        return confidence, outcome
