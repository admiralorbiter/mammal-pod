"""Item bank file loaders, parsers, and directory traversal utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_item_file(file_path: str | Path) -> list[dict[str, Any]]:
    """Load items from a single JSON or YAML file.
    
    Supports both a JSON/YAML array of items, or a single item dict, or a dict with an 'items' list.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Item bank file not found: {path}")

    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)

    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        if "items" in data and isinstance(data["items"], list):
            return data["items"]
        return [data]
    else:
        raise ValueError(f"Unexpected data format in {path}: expected list or dict, got {type(data)}")


def load_item_banks_from_directory(dir_path: str | Path) -> list[dict[str, Any]]:
    """Recursively discover and parse all item bank JSON/YAML files in a directory."""
    path = Path(dir_path)
    if not path.is_dir():
        if path.is_file():
            return load_item_file(path)
        raise NotADirectoryError(f"Directory not found: {path}")

    all_items: list[dict[str, Any]] = []
    # Search for JSON, YAML, YML files
    for ext in ("*.json", "*.yaml", "*.yml"):
        for item_file in sorted(path.rglob(ext)):
            try:
                items = load_item_file(item_file)
                all_items.extend(items)
            except Exception as exc:
                raise RuntimeError(f"Failed to parse item file {item_file}: {exc}") from exc

    return all_items


def get_default_item_banks_dir() -> Path:
    """Get the standard item banks directory inside the repository."""
    repo_root = Path(__file__).resolve().parents[3]
    candidate = repo_root / "config" / "item_banks"
    if candidate.exists():
        return candidate
    return Path("config") / "item_banks"
