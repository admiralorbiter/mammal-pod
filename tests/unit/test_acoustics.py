"""Unit tests for acoustic DSP feature extraction and audio quality gating."""

from __future__ import annotations

import io
import wave
import numpy as np
import pytest

from mammal.processors.acoustics import extract_acoustic_features


def _create_synthetic_wav(freq_hz: float = 200.0, duration_sec: float = 1.0, sr: int = 16000, noise_amp: float = 0.01) -> bytes:
    """Generate a clean synthetic sine wave formatted as 16-bit PCM WAV."""
    t = np.linspace(0, duration_sec, int(sr * duration_sec), endpoint=False)
    samples = 0.6 * np.sin(2.0 * np.pi * freq_hz * t) + noise_amp * np.random.randn(len(t))
    samples_int16 = (samples * 32767).astype(np.int16)

    bio = io.BytesIO()
    with wave.open(bio, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(samples_int16.tobytes())
    return bio.getvalue()


def test_extract_acoustic_features_pure_tone_f0():
    # 220 Hz sine wave
    wav_bytes = _create_synthetic_wav(freq_hz=220.0, duration_sec=1.0)
    features = extract_acoustic_features(wav_bytes, target_sr=16000, trial_id="trl_sine_220")

    assert features.trial_id == "trl_sine_220"
    assert features.duration_ms == pytest.approx(1000.0, abs=50.0)
    # Autocorrelation should estimate F0 near 220 Hz (+- 5 Hz)
    assert features.mean_f0_hz == pytest.approx(220.0, abs=8.0)
    assert features.pitch_jitter_pct < 3.0
    assert features.quality_report.is_passed is True
    assert features.quality_report.snr_db > 15.0


def test_extract_acoustic_features_empty_audio_safe_fallback():
    features = extract_acoustic_features(b"", trial_id="trl_empty")
    assert features.trial_id == "trl_empty"
    assert features.quality_report.is_passed is False
    assert any("empty" in r.lower() or "near-silent" in r.lower() for r in features.quality_report.disqualification_reasons)
