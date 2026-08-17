"""ASR transcription adapters and factory."""

from __future__ import annotations

import io
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ASRResult:
    """Canonical result of speech-to-text transcription."""

    text: str
    confidence: float
    duration_s: float
    processor_version: str
    language: str = "en"
    segments: list[dict[str, Any]] = field(default_factory=list)


class ASRAdapter(ABC):
    """Abstract interface for speech transcription engines."""

    @abstractmethod
    def transcribe(self, audio_bytes: bytes, mime_type: str = "audio/webm") -> ASRResult:
        """Transcribe audio bytes to text."""
        pass


class MockASRAdapter(ASRAdapter):
    """Deterministic ASR adapter for testing and offline qualification."""

    def __init__(self, default_text: str = "Paris", confidence: float = 0.98) -> None:
        self.default_text = default_text
        self.confidence = confidence
        self.processor_version = "mock-asr-v1.0"

    def transcribe(self, audio_bytes: bytes, mime_type: str = "audio/webm") -> ASRResult:
        if not audio_bytes:
            raise ValueError("Cannot transcribe empty audio buffer.")
        return ASRResult(
            text=self.default_text,
            confidence=self.confidence,
            duration_s=1.5,
            processor_version=self.processor_version,
            language="en",
            segments=[{"text": self.default_text, "start": 0.0, "end": 1.5}],
        )


class FasterWhisperAdapter(ASRAdapter):
    """Local ASR adapter utilizing faster-whisper CTranslate2 runtime."""

    def __init__(
        self,
        model_size: str = "tiny.en",
        device: str = "cpu",
        compute_type: str = "int8",
    ) -> None:
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.processor_version = f"faster-whisper-{model_size}"
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                from faster_whisper import WhisperModel
                self._model = WhisperModel(
                    self.model_size,
                    device=self.device,
                    compute_type=self.compute_type,
                )
            except Exception as exc:
                raise RuntimeError(f"Failed to load faster-whisper model '{self.model_size}': {exc}")
        return self._model

    def transcribe(self, audio_bytes: bytes, mime_type: str = "audio/webm") -> ASRResult:
        if not audio_bytes:
            raise ValueError("Cannot transcribe empty audio buffer.")

        model = self._get_model()

        # Write to temporary file for robust ffmpeg audio decoding
        suffix = ".webm" if "webm" in mime_type else ".wav"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            segments, info = model.transcribe(tmp_path, beam_size=5, language="en")
            collected_segments = []
            text_parts = []
            prob_sum = 0.0
            seg_count = 0

            for seg in segments:
                text_parts.append(seg.text.strip())
                prob_sum += getattr(seg, "avg_logprob", 0.0)
                seg_count += 1
                collected_segments.append({
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text.strip(),
                })

            full_text = " ".join(text_parts).strip()
            # Convert avg log probability to confidence approx in [0, 1]
            confidence = min(1.0, max(0.0, 1.0 + (prob_sum / max(1, seg_count)) / 5.0)) if seg_count else 0.9

            return ASRResult(
                text=full_text,
                confidence=confidence,
                duration_s=info.duration if hasattr(info, "duration") else 0.0,
                processor_version=self.processor_version,
                language=getattr(info, "language", "en"),
                segments=collected_segments,
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)


def get_asr_adapter(name: str = "mock", **kwargs: Any) -> ASRAdapter:
    """Factory helper to obtain an ASR adapter instance."""
    if name == "mock":
        return MockASRAdapter(**kwargs)
    elif name == "faster-whisper":
        return FasterWhisperAdapter(**kwargs)
    else:
        raise ValueError(f"Unknown ASR adapter: {name}")
