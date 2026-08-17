"""Adaptive psychophysical staircase algorithm for perceptual threshold estimation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import numpy as np


@dataclass
class StaircaseState:
    """Current state and trial history of an adaptive psychophysical staircase."""

    current_val: float
    step_size: float
    consecutive_correct: int
    n_down: int
    n_up: int
    reversal_count: int
    history_values: list[float] = field(default_factory=list)
    history_correct: list[bool] = field(default_factory=list)
    reversal_values: list[float] = field(default_factory=list)
    is_finished: bool = False
    estimated_threshold: float | None = None


class TransformedStaircase:
    """1-up / N-down transformed adaptive staircase (Levitt 1971)."""

    def __init__(
        self,
        initial_val: float = 0.50,
        n_down: int = 2,
        n_up: int = 1,
        initial_step_size: float = 0.08,
        min_step_size: float = 0.01,
        step_factor: float = 0.5,
        min_val: float = 0.01,
        max_val: float = 1.00,
        max_reversals: int = 8,
        max_trials: int = 60,
    ) -> None:
        self.initial_val = initial_val
        self.n_down = n_down
        self.n_up = n_up
        self.initial_step_size = initial_step_size
        self.min_step_size = min_step_size
        self.step_factor = step_factor
        self.min_val = min_val
        self.max_val = max_val
        self.max_reversals = max_reversals
        self.max_trials = max_trials

        self.current_val = initial_val
        self.step_size = initial_step_size
        self.consecutive_correct = 0
        self.last_direction: int = 0  # +1 (made harder/down), -1 (made easier/up), 0 (none)
        self.history_values: list[float] = []
        self.history_correct: list[bool] = []
        self.reversal_values: list[float] = []
        self.reversal_count = 0
        self.is_finished = False

    def step(self, is_correct: bool) -> StaircaseState:
        """Process response for the current trial and update staircase parameters."""
        if self.is_finished:
            return self.get_state()

        self.history_values.append(round(self.current_val, 4))
        self.history_correct.append(is_correct)

        new_direction = 0

        if is_correct:
            self.consecutive_correct += 1
            if self.consecutive_correct >= self.n_down:
                # Decrease coherence (make harder)
                new_direction = -1
                self.consecutive_correct = 0
                self.current_val -= self.step_size
        else:
            # Increase coherence (make easier)
            self.consecutive_correct = 0
            new_direction = +1
            self.current_val += self.step_size

        # Clamp value within bounds
        self.current_val = max(self.min_val, min(self.max_val, self.current_val))

        # Check for reversal in direction
        if new_direction != 0:
            if self.last_direction != 0 and new_direction != self.last_direction:
                self.reversal_count += 1
                self.reversal_values.append(round(self.history_values[-1], 4))
                # Reduce step size
                self.step_size = max(self.min_step_size, self.step_size * self.step_factor)
            self.last_direction = new_direction

        # Check termination criteria
        if self.reversal_count >= self.max_reversals or len(self.history_values) >= self.max_trials:
            self.is_finished = True

        return self.get_state()

    def get_threshold(self, last_n_reversals: int = 4) -> float | None:
        """Estimate perceptual threshold from the mean of the final N reversals."""
        if not self.reversal_values:
            return None
        k = min(len(self.reversal_values), last_n_reversals)
        return float(np.mean(self.reversal_values[-k:]))

    def get_state(self) -> StaircaseState:
        """Return the current snapshot of the staircase state."""
        threshold = self.get_threshold()
        return StaircaseState(
            current_val=round(self.current_val, 4),
            step_size=round(self.step_size, 4),
            consecutive_correct=self.consecutive_correct,
            n_down=self.n_down,
            n_up=self.n_up,
            reversal_count=self.reversal_count,
            history_values=list(self.history_values),
            history_correct=list(self.history_correct),
            reversal_values=list(self.reversal_values),
            is_finished=self.is_finished,
            estimated_threshold=round(threshold, 4) if threshold is not None else None,
        )
