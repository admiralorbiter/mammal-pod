"""Unit tests for ASR adapters and transcription factory."""

from __future__ import annotations

import pytest

from mammal.processors.asr import (
    FasterWhisperAdapter,
    MockASRAdapter,
    get_asr_adapter,
)


def test_mock_asr_adapter():
    adapter = MockASRAdapter(default_text="Whales breathe air", confidence=0.99)
    res = adapter.transcribe(b"fake audio stream bytes", mime_type="audio/webm")

    assert res.text == "Whales breathe air"
    assert res.confidence == 0.99
    assert res.duration_s == 1.5
    assert res.processor_version == "mock-asr-v1.0"
    assert len(res.segments) == 1


def test_mock_asr_empty_bytes_raises():
    adapter = MockASRAdapter()
    with pytest.raises(ValueError, match="Cannot transcribe empty"):
        adapter.transcribe(b"")


def test_get_asr_adapter_factory():
    mock = get_asr_adapter("mock", default_text="Paris")
    assert isinstance(mock, MockASRAdapter)
    assert mock.default_text == "Paris"

    whisper = get_asr_adapter("faster-whisper", model_size="tiny.en")
    assert isinstance(whisper, FasterWhisperAdapter)
    assert whisper.model_size == "tiny.en"

    with pytest.raises(ValueError, match="Unknown ASR adapter"):
        get_asr_adapter("non_existent_engine")
