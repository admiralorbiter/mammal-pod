"""Display qualification, hardware telemetry, and visual condition tracking for psychophysics."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import numpy as np


@dataclass
class VisualConditionRecord:
    """Visual acuity and observer condition during perceptual sessions (AGENTS.md Rule 10)."""

    visual_condition: str  # 'corrected_glasses', 'corrected_contacts', 'uncorrected'
    viewing_distance_cm: float
    viewing_eye: str = "binocular"  # 'binocular', 'left_eye', 'right_eye'
    ambient_lighting: str = "dim_controlled"  # 'dim_controlled', 'normal_office', 'dark'
    notes: str | None = None


@dataclass
class DisplayQualificationResult:
    """Telemetry report for display hardware timing and refresh stability (P00 Gate)."""

    viewport_width: int
    viewport_height: int
    device_pixel_ratio: float
    fullscreen: bool
    estimated_refresh_rate_hz: float
    total_frames_tested: int
    dropped_frames_count: int
    dropped_frames_pct: float
    frame_jitter_std_ms: float
    is_qualified: bool
    disqualifying_reasons: list[str] = field(default_factory=list)
    tested_at: str = ""


def qualify_display(
    frame_intervals_ms: list[float],
    viewport_width: int,
    viewport_height: int,
    device_pixel_ratio: float,
    fullscreen: bool,
    max_jitter_ms: float = 4.0,
    max_dropped_pct: float = 2.0,
) -> DisplayQualificationResult:
    """Evaluate frame timing stream against scientific display qualification standards (P00 Gate)."""
    if len(frame_intervals_ms) < 30:
        return DisplayQualificationResult(
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            device_pixel_ratio=device_pixel_ratio,
            fullscreen=fullscreen,
            estimated_refresh_rate_hz=0.0,
            total_frames_tested=len(frame_intervals_ms),
            dropped_frames_count=0,
            dropped_frames_pct=100.0,
            frame_jitter_std_ms=999.0,
            is_qualified=False,
            disqualifying_reasons=["Insufficient frame samples collected (< 30 frames)."],
            tested_at=datetime.utcnow().isoformat() + "Z",
        )

    intervals = np.array(frame_intervals_ms, dtype=float)
    median_interval = float(np.median(intervals))

    if median_interval <= 0.0:
        estimated_hz = 60.0
    else:
        estimated_hz = round(1000.0 / median_interval, 1)

    expected_interval = 1000.0 / estimated_hz if estimated_hz > 0 else 16.67
    jitter_std = float(np.std(intervals))

    # A frame is considered dropped if it exceeds 1.5x expected interval
    dropped = int(np.sum(intervals > (1.5 * expected_interval)))
    dropped_pct = float((dropped / len(intervals)) * 100.0)

    reasons: list[str] = []
    if dropped_pct > max_dropped_pct:
        reasons.append(f"Dropped frame rate ({dropped_pct:.1f}%) exceeded maximum allowed ({max_dropped_pct}%).")
    if jitter_std > max_jitter_ms:
        reasons.append(f"Frame timing jitter standard deviation ({jitter_std:.2f}ms) exceeded threshold ({max_jitter_ms}ms).")
    if not fullscreen:
        reasons.append("Display was not in true fullscreen mode during qualification.")

    is_qualified = len(reasons) == 0

    return DisplayQualificationResult(
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        device_pixel_ratio=device_pixel_ratio,
        fullscreen=fullscreen,
        estimated_refresh_rate_hz=estimated_hz,
        total_frames_tested=len(frame_intervals_ms),
        dropped_frames_count=dropped,
        dropped_frames_pct=round(dropped_pct, 2),
        frame_jitter_std_ms=round(jitter_std, 2),
        is_qualified=is_qualified,
        disqualifying_reasons=reasons,
        tested_at=datetime.utcnow().isoformat() + "Z",
    )
