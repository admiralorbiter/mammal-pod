"""Processors and analysis pipeline exports."""

from mammal.processors.asr import (
    ASRAdapter,
    ASRResult,
    FasterWhisperAdapter,
    MockASRAdapter,
    get_asr_adapter,
)

__all__ = [
    "ASRResult",
    "ASRAdapter",
    "MockASRAdapter",
    "FasterWhisperAdapter",
    "get_asr_adapter",
]
