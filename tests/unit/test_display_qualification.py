"""Unit tests for P00 display timing qualification and visual hardware audit."""

from __future__ import annotations

import numpy as np
import pytest

from mammal.psychophysics.display import qualify_display


def test_qualify_display_ideal_60hz():
    # 120 frames at exactly 16.67ms (60 FPS) with small random micro-jitter (~0.2ms)
    rng = np.random.default_rng(42)
    intervals = [16.67 + float(rng.normal(0, 0.2)) for _ in range(120)]

    res = qualify_display(
        frame_intervals_ms=intervals,
        viewport_width=1920,
        viewport_height=1080,
        device_pixel_ratio=1.0,
        fullscreen=True,
    )

    assert res.is_qualified is True
    assert res.estimated_refresh_rate_hz == pytest.approx(60.0, abs=1.5)
    assert res.dropped_frames_count == 0
    assert res.frame_jitter_std_ms < 1.0
    assert len(res.disqualifying_reasons) == 0


def test_qualify_display_ideal_120hz():
    # 150 frames at 8.33ms (120 FPS)
    intervals = [8.33 for _ in range(150)]

    res = qualify_display(
        frame_intervals_ms=intervals,
        viewport_width=2560,
        viewport_height=1440,
        device_pixel_ratio=2.0,
        fullscreen=True,
    )

    assert res.is_qualified is True
    assert res.estimated_refresh_rate_hz == pytest.approx(120.0, abs=1.0)
    assert res.dropped_frames_count == 0


def test_qualify_display_fails_dropped_frames():
    # 100 frames with 10 dropped frames (33.3ms intervals)
    intervals = [16.67] * 90 + [33.34] * 10

    res = qualify_display(
        frame_intervals_ms=intervals,
        viewport_width=1920,
        viewport_height=1080,
        device_pixel_ratio=1.0,
        fullscreen=True,
        max_dropped_pct=2.0,
    )

    assert res.is_qualified is False
    assert res.dropped_frames_count == 10
    assert any("Dropped frame rate" in r for r in res.disqualifying_reasons)


def test_qualify_display_fails_not_fullscreen():
    intervals = [16.67 for _ in range(100)]

    res = qualify_display(
        frame_intervals_ms=intervals,
        viewport_width=1280,
        viewport_height=720,
        device_pixel_ratio=1.0,
        fullscreen=False,
    )

    assert res.is_qualified is False
    assert any("fullscreen" in r.lower() for r in res.disqualifying_reasons)
