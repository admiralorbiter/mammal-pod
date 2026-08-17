"""Project MAMMAL Statistical Analysis and Metacognitive Estimands Kernel."""

from mammal.analysis.bootstrap import block_bootstrap_ci
from mammal.analysis.engine import AnalysisResult, analyze_episode, generate_analysis_report
from mammal.analysis.manifest import FrozenTargetManifest, TargetTrialRecord, create_frozen_target_manifest
from mammal.analysis.metrics import (
    compute_accuracy,
    compute_auroc2,
    compute_brier_score,
    compute_expected_calibration_error,
    compute_type2_sdt,
)
from mammal.analysis.precision_planner import PrecisionPlanResult, plan_session_precision

__all__ = [
    "compute_accuracy",
    "compute_brier_score",
    "compute_expected_calibration_error",
    "compute_auroc2",
    "compute_type2_sdt",
    "block_bootstrap_ci",
    "analyze_episode",
    "generate_analysis_report",
    "AnalysisResult",
    "create_frozen_target_manifest",
    "FrozenTargetManifest",
    "TargetTrialRecord",
    "plan_session_precision",
    "PrecisionPlanResult",
]
