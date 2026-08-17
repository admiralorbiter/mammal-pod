"""Session-preserving block bootstrap resampling for empirical confidence intervals."""

from __future__ import annotations

from typing import Any, Callable, Sequence
import numpy as np


def block_bootstrap_ci(
    data: Sequence[dict[str, Any]],
    metric_fn: Callable[[list[dict[str, Any]]], float],
    block_size: int = 5,
    n_resamples: int = 500,
    alpha: float = 0.05,
    seed: int = 42,
) -> tuple[float, float, float]:
    """Compute point estimate and (1-alpha) empirical confidence interval using block bootstrap."""
    if not data:
        return 0.0, 0.0, 0.0

    point_estimate = float(metric_fn(list(data)))
    n = len(data)

    if n < block_size or n < 4:
        # Too few items for resampling; return point estimate
        return point_estimate, point_estimate, point_estimate

    rng = np.random.default_rng(seed)
    effective_block_size = max(1, min(block_size, n // 2))
    n_blocks_needed = int(np.ceil(n / effective_block_size))

    # Construct overlapping blocks
    blocks: list[list[dict[str, Any]]] = []
    for i in range(n - effective_block_size + 1):
        blocks.append(list(data[i : i + effective_block_size]))

    bootstrap_estimates: list[float] = []

    for _ in range(n_resamples):
        sampled_block_indices = rng.choice(len(blocks), size=n_blocks_needed, replace=True)
        resampled_items: list[dict[str, Any]] = []
        for idx in sampled_block_indices:
            resampled_items.extend(blocks[idx])
        # Trim to exact length n
        resampled_sample = resampled_items[:n]

        try:
            val = float(metric_fn(resampled_sample))
            if not np.isnan(val):
                bootstrap_estimates.append(val)
        except Exception:
            continue

    if not bootstrap_estimates:
        return point_estimate, point_estimate, point_estimate

    lower_pct = (alpha / 2.0) * 100.0
    upper_pct = (1.0 - alpha / 2.0) * 100.0

    ci_lower = float(np.percentile(bootstrap_estimates, lower_pct))
    ci_upper = float(np.percentile(bootstrap_estimates, upper_pct))

    return point_estimate, ci_lower, ci_upper
