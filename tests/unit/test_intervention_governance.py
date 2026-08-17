"""Unit tests for S3 and Venom intervention governance safety rules."""

from __future__ import annotations

from mammal.interventions.governance import InterventionGovernanceGuard


def test_observation_mode_strictly_forbids_interventions():
    # In Observation Mode without protocol override, no intervention is permitted
    res = InterventionGovernanceGuard.validate_intervention(
        message="The model estimates 80% confidence.",
        session_mode="observation",
        protocol_allows_feedback=False,
    )
    assert res.is_approved is False
    assert any("Rule 6 Violation" in v for v in res.violations)


def test_reject_identity_level_trait_claims():
    # Forbidden identity statements must be blocked
    toxic_msg = "You are inherently bad at world geography."
    res = InterventionGovernanceGuard.validate_intervention(
        message=toxic_msg,
        session_mode="intervention",
        protocol_allows_feedback=True,
    )
    assert res.is_approved is False
    assert any("Rule 5 Violation" in v for v in res.violations)


def test_approve_epistemically_hedged_intervention():
    # Valid epistemic model disclosure during intervention mode
    valid_msg = "Across currently observed trials, the model estimates a 78% probability of correctness."
    res = InterventionGovernanceGuard.validate_intervention(
        message=valid_msg,
        session_mode="intervention",
        protocol_allows_feedback=True,
    )
    assert res.is_approved is True
    assert len(res.violations) == 0
    assert res.sanitized_message == valid_msg
