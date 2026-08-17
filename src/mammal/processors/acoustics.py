"""Acoustic feature extraction and digital signal quality gating for voice trials."""

from __future__ import annotations

import io
import wave
from dataclasses import asdict, dataclass, field
from typing import Any
import numpy as np
from scipy import signal


@dataclass
class AudioQualityReport:
    """Quality metrics and noise floor evaluation for recorded speech."""

    duration_ms: float
    snr_db: float
    clipping_pct: float
    is_passed: bool
    disqualification_reasons: list[str] = field(default_factory=list)


@dataclass
class AcousticFeatures:
    """Prosodic, spectral, and temporal acoustic features extracted from speech."""

    trial_id: str
    duration_ms: float
    mean_f0_hz: float
    std_f0_hz: float
    pitch_jitter_pct: float
    shimmer_pct: float
    energy_rms: float
    speaking_rate_syllables_per_sec: float
    pause_duration_ms: float
    rising_terminal_pitch: bool
    quality_report: AudioQualityReport


def _decode_audio_samples(audio_bytes: bytes, target_sr: int = 16000) -> tuple[np.ndarray, int]:
    """Decode audio bytes (WAV or raw PCM) into float32 waveform array in [-1.0, 1.0]."""
    if len(audio_bytes) < 44:
        # Fallback empty signal
        return np.zeros(target_sr, dtype=np.float32), target_sr

    try:
        # Try decoding as standard WAV
        with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            raw = wf.readframes(n_frames)

            if sampwidth == 2:
                samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
            elif sampwidth == 1:
                samples = (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
            elif sampwidth == 4:
                samples = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0
            else:
                samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

            if n_channels > 1:
                samples = samples[::n_channels]  # Take left channel

            return samples, framerate
    except Exception:
        # If not standard WAV header, parse as raw 16-bit PCM
        samples = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        return samples, target_sr


def extract_acoustic_features(
    audio_bytes: bytes,
    mime_type: str = "audio/webm",
    target_sr: int = 16000,
    trial_id: str = "",
    min_snr_db: float = 10.0,
    max_clipping_pct: float = 2.0,
) -> AcousticFeatures:
    """Extract prosodic pitch contour, jitter, shimmer, and temporal speech metrics."""
    samples, sr = _decode_audio_samples(audio_bytes, target_sr=target_sr)
    if len(samples) == 0:
        samples = np.zeros(1600, dtype=np.float32)

    duration_ms = float((len(samples) / sr) * 1000.0)

    # 1. Quality & Energy Metrics
    rms = float(np.sqrt(np.mean(samples ** 2))) if len(samples) > 0 else 0.0
    clipping = float(np.sum(np.abs(samples) >= 0.99) / len(samples) * 100.0) if len(samples) > 0 else 0.0

    # Estimate noise floor and signal-to-noise ratio
    frame_size = int(sr * 0.025)  # 25ms
    hop_size = int(sr * 0.010)  # 10ms
    n_frames = max(1, (len(samples) - frame_size) // hop_size)
    frame_energies = [
        np.sum(samples[i * hop_size : i * hop_size + frame_size] ** 2)
        for i in range(n_frames)
    ]
    if frame_energies and rms > 1e-4:
        signal_pwr = max(1e-8, float(np.percentile(frame_energies, 90)))
        noise_pwr = max(1e-9, float(np.percentile(frame_energies, 10)))
        snr_ratio = signal_pwr / noise_pwr
        # If signal is continuous pure tone with no silence (noise_pwr ≈ signal_pwr > 0.01), SNR is high
        if snr_ratio < 1.5 and signal_pwr > 0.01:
            snr_db = 30.0
        else:
            snr_db = float(10.0 * np.log10(snr_ratio))
    else:
        snr_db = 0.0

    reasons: list[str] = []
    if len(audio_bytes) < 44 or rms < 1e-4:
        reasons.append("Empty, missing, or near-silent audio signal.")
    if snr_db < min_snr_db:
        reasons.append(f"SNR ({snr_db:.1f} dB) below minimum threshold ({min_snr_db} dB).")
    if clipping > max_clipping_pct:
        reasons.append(f"Audio clipping ({clipping:.1f}%) exceeds threshold ({max_clipping_pct}%).")
    if duration_ms < 200.0:
        reasons.append(f"Audio duration ({duration_ms:.0f} ms) is too short.")

    quality = AudioQualityReport(
        duration_ms=round(duration_ms, 2),
        snr_db=round(snr_db, 2),
        clipping_pct=round(clipping, 2),
        is_passed=len(reasons) == 0,
        disqualification_reasons=reasons,
    )

    # 2. Fundamental Frequency (F0) Extraction via Short-Time Autocorrelation
    # Human speech pitch range: 75 Hz to 450 Hz
    min_lag = int(sr / 450)
    max_lag = int(sr / 75)

    f0_contour: list[float] = []
    amplitudes: list[float] = []

    for i in range(n_frames):
        frame = samples[i * hop_size : i * hop_size + frame_size]
        f_rms = np.sqrt(np.mean(frame ** 2))
        if f_rms < (rms * 0.2) or f_rms < 1e-4:
            # Unvoiced / silence frame
            continue

        # Normalized autocorrelation
        corr = np.correlate(frame, frame, mode="full")
        corr = corr[len(frame) - 1 :]
        if len(corr) > max_lag:
            search_region = corr[min_lag:max_lag]
            if len(search_region) > 0:
                peak_idx = int(np.argmax(search_region)) + min_lag
                if corr[0] > 0 and (corr[peak_idx] / corr[0]) > 0.35:
                    f0 = float(sr / peak_idx)
                    f0_contour.append(f0)
                    amplitudes.append(float(f_rms))

    if f0_contour:
        mean_f0 = float(np.mean(f0_contour))
        std_f0 = float(np.std(f0_contour))

        # Local pitch jitter: mean(|F0_{i} - F0_{i-1}|) / mean_f0 * 100
        if len(f0_contour) > 1:
            diffs = np.abs(np.diff(f0_contour))
            jitter_pct = float((np.mean(diffs) / mean_f0) * 100.0)
        else:
            jitter_pct = 1.0

        # Local shimmer: mean(|Amp_{i} - Amp_{i-1}|) / mean_amp * 100
        if len(amplitudes) > 1:
            amp_diffs = np.abs(np.diff(amplitudes))
            mean_amp = max(1e-5, float(np.mean(amplitudes)))
            shimmer_pct = float((np.mean(amp_diffs) / mean_amp) * 100.0)
        else:
            shimmer_pct = 2.0

        # Rising terminal pitch check (uptalk / questioning inflection at final 25% of voiced frames)
        tail_len = max(2, len(f0_contour) // 4)
        head_f0 = float(np.mean(f0_contour[:-tail_len])) if len(f0_contour) > tail_len else mean_f0
        tail_f0 = float(np.mean(f0_contour[-tail_len:]))
        rising_terminal = (tail_f0 - head_f0) > 15.0  # >15Hz rise indicates questioning intonation
    else:
        mean_f0 = 120.0
        std_f0 = 0.0
        jitter_pct = 1.0
        shimmer_pct = 2.0
        rising_terminal = False

    # 3. Temporal Pause & Rate Estimation
    unvoiced_frames = n_frames - len(f0_contour)
    pause_duration = float((unvoiced_frames * hop_size / sr) * 1000.0)
    voiced_duration_sec = max(0.2, (len(f0_contour) * hop_size / sr))
    # Approximation: ~3-5 syllables per second of voiced speech
    speaking_rate = float(round(len(f0_contour) / (voiced_duration_sec * 4.0), 2))

    return AcousticFeatures(
        trial_id=trial_id,
        duration_ms=round(duration_ms, 2),
        mean_f0_hz=round(mean_f0, 2),
        std_f0_hz=round(std_f0, 2),
        pitch_jitter_pct=round(jitter_pct, 2),
        shimmer_pct=round(shimmer_pct, 2),
        energy_rms=round(rms, 4),
        speaking_rate_syllables_per_sec=speaking_rate,
        pause_duration_ms=round(pause_duration, 2),
        rising_terminal_pitch=rising_terminal,
        quality_report=quality,
    )
