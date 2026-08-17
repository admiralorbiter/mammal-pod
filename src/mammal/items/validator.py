"""Validation and quality-guard engine for Project MAMMAL item banks."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jsonschema.validators import Draft202012Validator

from mammal.items.bank import get_item_schema


@dataclass
class ItemValidationIssue:
    """Individual validation failure or warning for an item."""
    item_id: str
    issue_type: str  # "error" | "warning"
    message: str
    field_name: str | None = None


@dataclass
class ItemBankValidationReport:
    """Comprehensive audit report for an item bank or directory of items."""
    total_items: int = 0
    valid_items: int = 0
    invalid_items: int = 0
    errors: list[ItemValidationIssue] = field(default_factory=list)
    warnings: list[ItemValidationIssue] = field(default_factory=list)
    domain_counts: dict[str, int] = field(default_factory=dict)
    family_counts: dict[str, int] = field(default_factory=dict)
    partition_counts: dict[str, int] = field(default_factory=dict)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


class ItemValidator:
    """Validator enforcing schema conformance, option homogeneity, and partition isolation."""

    def __init__(self, schema: dict[str, Any] | None = None) -> None:
        self.schema = schema or get_item_schema()
        self.validator = Draft202012Validator(self.schema)

    def validate_item(self, item: dict[str, Any]) -> tuple[list[ItemValidationIssue], list[ItemValidationIssue]]:
        """Validate a single item dict. Returns (errors, warnings)."""
        errors: list[ItemValidationIssue] = []
        warnings: list[ItemValidationIssue] = []
        item_id = item.get("item_id", "UNKNOWN_ITEM")

        # 1. JSON Schema Conformance
        for err in self.validator.iter_errors(item):
            path_str = ".".join(str(p) for p in err.path)
            errors.append(
                ItemValidationIssue(
                    item_id=item_id,
                    issue_type="error",
                    message=f"Schema violation: {err.message}",
                    field_name=path_str,
                )
            )

        # 2. Options and Ground Truth Verification
        options = item.get("options")
        gt = item.get("ground_truth")

        if options is not None:
            if not isinstance(options, list) or len(options) < 2:
                errors.append(
                    ItemValidationIssue(
                        item_id=item_id,
                        issue_type="error",
                        message=f"Options must be a list of at least 2 choices, got {len(options) if isinstance(options, list) else type(options)}",
                        field_name="options",
                    )
                )
            else:
                # Check for duplicate options
                str_opts = [str(o).strip().lower() for o in options]
                if len(str_opts) != len(set(str_opts)):
                    errors.append(
                        ItemValidationIssue(
                            item_id=item_id,
                            issue_type="error",
                            message="Options list contains duplicate choices",
                            field_name="options",
                        )
                    )

                # Check ground truth consistency
                if isinstance(gt, dict):
                    canonical = gt.get("canonical")
                    opt_idx = gt.get("option_index")

                    if canonical is not None:
                        canonical_str = str(canonical).strip().lower()
                        if canonical_str not in str_opts:
                            errors.append(
                                ItemValidationIssue(
                                    item_id=item_id,
                                    issue_type="error",
                                    message=f"Ground truth canonical value '{canonical}' not found in options {options}",
                                    field_name="ground_truth.canonical",
                                )
                            )

                    if opt_idx is not None:
                        if not isinstance(opt_idx, int) or opt_idx < 0 or opt_idx >= len(options):
                            errors.append(
                                ItemValidationIssue(
                                    item_id=item_id,
                                    issue_type="error",
                                    message=f"Ground truth option_index {opt_idx} is out of bounds for options length {len(options)}",
                                    field_name="ground_truth.option_index",
                                )
                            )
                        elif canonical is not None:
                            expected_at_idx = str(options[opt_idx]).strip().lower()
                            if expected_at_idx != str(canonical).strip().lower():
                                errors.append(
                                    ItemValidationIssue(
                                        item_id=item_id,
                                        issue_type="error",
                                        message=f"Ground truth option_index {opt_idx} points to '{options[opt_idx]}', does not match canonical '{canonical}'",
                                        field_name="ground_truth",
                                    )
                                )
                elif isinstance(gt, str):
                    if gt.strip().lower() not in str_opts:
                        errors.append(
                            ItemValidationIssue(
                                item_id=item_id,
                                issue_type="error",
                                message=f"Ground truth '{gt}' not found in options",
                                field_name="ground_truth",
                            )
                        )

                # 3. Distractor Balance & Length Outlier Warning
                if len(options) >= 2 and all(isinstance(o, str) for o in options):
                    lens = [len(o) for o in options]
                    avg_len = sum(lens) / len(lens)
                    for idx, l in enumerate(lens):
                        if avg_len > 10 and l > 3.5 * avg_len:
                            warnings.append(
                                ItemValidationIssue(
                                    item_id=item_id,
                                    issue_type="warning",
                                    message=f"Option {idx} ('{options[idx]}') length ({l}) is significantly longer than mean ({avg_len:.1f}), which may act as a heuristic cue.",
                                    field_name=f"options[{idx}]",
                                )
                            )

        # 4. Source & Provenance
        src = item.get("source")
        if isinstance(src, dict) and not src.get("provenance"):
            errors.append(
                ItemValidationIssue(
                    item_id=item_id,
                    issue_type="error",
                    message="Missing required 'provenance' field in source metadata",
                    field_name="source.provenance",
                )
            )

        return errors, warnings

    def validate_items(self, items: list[dict[str, Any]]) -> ItemBankValidationReport:
        """Validate a collection of items and check for cross-item collisions."""
        report = ItemBankValidationReport(total_items=len(items))

        seen_ids: dict[str, int] = {}
        seen_prompts: dict[str, str] = {}  # prompt_text -> partition

        for item in items:
            item_id = item.get("item_id", "UNKNOWN_ITEM")
            domain = item.get("domain", "unknown")
            family = item.get("family", "unknown")
            partition = item.get("partition", "unknown")

            report.domain_counts[domain] = report.domain_counts.get(domain, 0) + 1
            report.family_counts[family] = report.family_counts.get(family, 0) + 1
            report.partition_counts[partition] = report.partition_counts.get(partition, 0) + 1

            # Check duplicate ID
            if item_id in seen_ids:
                report.errors.append(
                    ItemValidationIssue(
                        item_id=item_id,
                        issue_type="error",
                        message=f"Duplicate item_id '{item_id}' detected",
                        field_name="item_id",
                    )
                )
            else:
                seen_ids[item_id] = 1

            # Check prompt cross-partition leakage
            prompt_obj = item.get("prompt")
            prompt_str = ""
            if isinstance(prompt_obj, str):
                prompt_str = prompt_obj.strip().lower()
            elif isinstance(prompt_obj, dict):
                prompt_str = prompt_obj.get("question", prompt_obj.get("study_text", str(prompt_obj))).strip().lower()

            if prompt_str:
                if prompt_str in seen_prompts:
                    prev_part = seen_prompts[prompt_str]
                    if prev_part != partition:
                        report.errors.append(
                            ItemValidationIssue(
                                item_id=item_id,
                                issue_type="error",
                                message=f"Prompt collision across partitions: prompt already exists in '{prev_part}' partition, now seen in '{partition}'",
                                field_name="prompt",
                            )
                        )
                else:
                    seen_prompts[prompt_str] = partition

            # Item-level validation
            item_errors, item_warnings = self.validate_item(item)
            report.errors.extend(item_errors)
            report.warnings.extend(item_warnings)

            if len(item_errors) == 0:
                report.valid_items += 1
            else:
                report.invalid_items += 1

        return report
