"""Audio leakage gain analysis quantifying metacognitive signal in acoustic prosody."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AudioLeakageReport:
    """Evaluation of how much subjective confidence information leaks into public acoustic speech signals."""

    episode_id: str
    text_observer_brier: float
    acoustic_observer_brier: float
    delta_brier_gain: float  # Brier_Text - Brier_Acoustic (positive means acoustics improved prediction)
    audio_leakage_gain_pct: float  # (Brier_Text - Brier_Acoustic) / Brier_Text * 100
    text_auroc2: float
    acoustic_auroc2: float
    delta_auroc2_gain: float  # AUROC2_Acoustic - AUROC2_Text
    public_signal_verdict: str


def compute_audio_leakage_gain(
    episode_id: str,
    text_brier: float,
    acoustic_brier: float,
    text_auroc2: float,
    acoustic_auroc2: float,
) -> AudioLeakageReport:
    """Compute relative performance gain from acoustic prosodic features over text alone."""
    delta_brier = text_brier - acoustic_brier
    gain_pct = (delta_brier / text_brier * 100.0) if text_brier > 1e-6 else 0.0
    delta_auroc = acoustic_auroc2 - text_auroc2

    if gain_pct > 5.0 and delta_auroc > 0.03:
        verdict = "Significant public acoustic confidence leakage detected (prosody predicts human certainty)."
    elif gain_pct > 0.0:
        verdict = "Modest acoustic leakage observed (slight improvement over text alone)."
    else:
        verdict = "No public acoustic leakage detected (prosody did not reduce prediction error)."

    return AudioLeakageReport(
        episode_id=episode_id,
        text_observer_brier=round(text_brier, 4),
        acoustic_observer_brier=round(acoustic_brier, 4),
        delta_brier_gain=round(delta_brier, 4),
        audio_leakage_gain_pct=round(gain_pct, 2),
        text_auroc2=round(text_auroc2, 4),
        acoustic_auroc2=round(acoustic_auroc2, 4),
        delta_auroc2_gain=round(delta_auroc, 4),
        public_signal_verdict=verdict,
    )
