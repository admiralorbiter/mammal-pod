"""Safety, ethics, and S3 governance guard enforcing epistemic separation and Observation Mode lockdown."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class GovernanceCheckResult:
    """Outcome of safety, ethics, and epistemic compliance auditing."""

    is_approved: bool
    violations: list[str] = field(default_factory=list)
    sanitized_message: str = ""


class InterventionGovernanceGuard:
    """S3 and Venom governance filter enforcing AGENTS.md Rules 5 and 6."""

    FORBIDDEN_IDENTITY_PATTERNS: list[re.Pattern] = [
        re.compile(r"\b(you are|jonathan is)\s+(inherently|naturally|fundamentally)\s+(bad|good|flawed|incapable)\b", re.I),
        re.compile(r"\b(you lack|lacks)\s+(intelligence|cognitive ability|competence)\b", re.I),
        re.compile(r"\b(you will never|hopeless|unfixable trait)\b", re.I),
        re.compile(r"\b(inherently bad at|inherently good at)\b", re.I),
    ]

    REQUIRED_EPISTEMIC_HEDGES: list[str] = [
        "model estimates",
        "across currently observed",
        "observed trials",
        "data indicates",
        "suggests",
        "statistical baseline",
        "model prediction",
        "historical average",
        "feedback:",
    ]

    @classmethod
    def validate_intervention(
        cls,
        message: str,
        session_mode: str,
        protocol_allows_feedback: bool = False,
    ) -> GovernanceCheckResult:
        """Audit feedback message before display to participant."""
        violations: list[str] = []

        # 1. AGENTS.md Rule 6: Observation Mode lockdown
        if session_mode.lower() == "observation" and not protocol_allows_feedback:
            violations.append(
                "Rule 6 Violation: Intervention forbidden during Observation Mode. "
                "Observation Mode must hide live coaching, model predictions, and conclusions."
            )

        # 2. AGENTS.md Rule 5: Identity-level trait claim prohibition
        for pattern in cls.FORBIDDEN_IDENTITY_PATTERNS:
            if pattern.search(message):
                violations.append(
                    f"Rule 5 Violation: Identity-level trait claim detected matching pattern '{pattern.pattern}'. "
                    "Do not write identity-level conclusions; state only what the model estimates across observed trials."
                )

        # 3. Epistemic framing check (if intervention message is non-empty)
        if message and not any(hedge in message.lower() for hedge in cls.REQUIRED_EPISTEMIC_HEDGES):
            # If plain correctness feedback ("Correct", "Incorrect"), allow it
            if message.strip().lower() not in {"correct", "incorrect", "pass", "time expired"}:
                violations.append(
                    "Rule 5 Warning: Feedback message lacks epistemic framing (e.g. 'Across observed trials, the model estimates...')."
                )

        is_approved = len(violations) == 0
        return GovernanceCheckResult(
            is_approved=is_approved,
            violations=violations,
            sanitized_message=message.strip() if is_approved else "",
        )
