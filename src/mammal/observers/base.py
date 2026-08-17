"""Base classes and schemas for external and statistical observers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from mammal.observers.contracts import VisibilityLevel


@dataclass
class ObserverPrediction:
    """Standardized output prediction for a single trial."""

    trial_id: str
    observer_id: str
    visibility_level: str
    predicted_answer: Any
    predicted_probability_correct: float  # In [0.0, 1.0]
    confidence: float  # Scaled to [0.0, 100.0]
    latency_ms: float
    raw_metadata: dict[str, Any] = field(default_factory=dict)


class ObserverAdapter(ABC):
    """Abstract interface for all statistical, heuristic, and model-based observers."""

    @property
    @abstractmethod
    def observer_id(self) -> str:
        """Unique identifier for this observer."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Version string of the observer implementation."""
        pass

    @property
    @abstractmethod
    def visibility_level(self) -> VisibilityLevel:
        """Visibility contract required by this observer."""
        pass

    @abstractmethod
    def predict(self, compiled_input: dict[str, Any]) -> ObserverPrediction:
        """Generate prediction from strictly compiled trial input."""
        pass
