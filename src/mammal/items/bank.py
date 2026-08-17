"""Item bank management, schema validation, and fixture seeding."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence

from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft202012Validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from mammal.artifacts.store import compute_sha256
from mammal.events.engine import canonical_json_dumps
from mammal.models.entities import Item


def get_item_schema() -> dict[str, Any]:
    """Load JSON schema for Project MAMMAL items."""
    schema_path = Path(__file__).resolve().parents[3] / "schemas" / "item.schema.json"
    if not schema_path.exists():
        schema_path = Path("schemas") / "item.schema.json"
    return json.loads(schema_path.read_text(encoding="utf-8"))


def compute_item_content_hash(item_data: dict[str, Any]) -> str:
    """Compute deterministic SHA-256 hash of immutable item contents."""
    canonical_repr = {
        "item_id": item_data["item_id"],
        "version": item_data["version"],
        "domain": item_data["domain"],
        "family": item_data["family"],
        "prompt": item_data["prompt"],
        "options": item_data.get("options"),
        "ground_truth": item_data["ground_truth"],
        "source": item_data["source"],
    }
    dumped = canonical_json_dumps(canonical_repr)
    return compute_sha256(dumped.encode("utf-8"))


def register_item(session: Session, item_data: dict[str, Any]) -> Item:
    """Validate and register an item into the database item bank."""
    schema = get_item_schema()
    validator = Draft202012Validator(schema)
    validator.validate(item_data)

    content_hash = compute_item_content_hash(item_data)
    item_id = item_data["item_id"]
    version = str(item_data["version"])

    stmt = select(Item).where(Item.item_id == item_id, Item.version == version)
    existing = session.scalars(stmt).first()

    if existing:
        return existing

    item = Item(
        item_id=item_id,
        version=version,
        domain=item_data["domain"],
        family=item_data["family"],
        prompt_json=item_data["prompt"],
        options_json=item_data.get("options"),
        ground_truth_json=item_data["ground_truth"],
        partition=item_data["partition"],
        source_json=item_data["source"],
        difficulty_json=item_data.get("difficulty"),
        verification_json=item_data.get("verification"),
        leakage_checks_json=item_data.get("leakage_checks"),
        content_hash=content_hash,
    )
    session.add(item)
    session.flush()
    return item


QUALIFICATION_FIXTURE_ITEMS: list[dict[str, Any]] = [
    {
        "item_id": "sem_geo_001",
        "version": "1.0.0",
        "domain": "semantic",
        "family": "world_geography",
        "prompt": {"question": "What is the capital city of France?"},
        "options": ["Lyon", "Marseille", "Paris", "Toulouse"],
        "ground_truth": {"canonical": "Paris", "option_index": 2},
        "partition": "engineering",
        "source": {"provenance": "synthetic_seed_v1", "license": "CC0"},
    },
    {
        "item_id": "sem_geo_002",
        "version": "1.0.0",
        "domain": "semantic",
        "family": "world_geography",
        "prompt": {"question": "Which river flows through Cairo?"},
        "options": ["Amazon", "Danube", "Nile", "Thames"],
        "ground_truth": {"canonical": "Nile", "option_index": 2},
        "partition": "engineering",
        "source": {"provenance": "synthetic_seed_v1", "license": "CC0"},
    },
    {
        "item_id": "sem_sci_001",
        "version": "1.0.0",
        "domain": "semantic",
        "family": "physical_science",
        "prompt": {"question": "What is the chemical symbol for Gold?"},
        "options": ["Ag", "Au", "Fe", "Pb"],
        "ground_truth": {"canonical": "Au", "option_index": 1},
        "partition": "engineering",
        "source": {"provenance": "synthetic_seed_v1", "license": "CC0"},
    },
    {
        "item_id": "form_logic_001",
        "version": "1.0.0",
        "domain": "formal_math_logic",
        "family": "propositional_logic",
        "prompt": {"question": "If 'All mammals breathe air' and 'Whales are mammals', what follows?"},
        "options": [
            "Whales breathe air",
            "Whales lay eggs",
            "Not all mammals are whales",
            "Air is made of mammals",
        ],
        "ground_truth": {"canonical": "Whales breathe air", "option_index": 0},
        "partition": "engineering",
        "source": {"provenance": "synthetic_seed_v1", "license": "CC0"},
    },
]


def seed_qualification_items(session: Session) -> list[Item]:
    """Ensure baseline qualification items are present in item bank."""
    registered = []
    for item_dict in QUALIFICATION_FIXTURE_ITEMS:
        item = register_item(session, item_dict)
        registered.append(item)
    return registered


def get_items_for_protocol(session: Session, partition: str = "engineering", limit: int = 10) -> Sequence[Item]:
    """Query available items for an experiment partition."""
    stmt = select(Item).where(Item.partition == partition).limit(limit)
    items = list(session.scalars(stmt).all())
    if not items:
        # Seed qualification items if empty
        seed_qualification_items(session)
        items = list(session.scalars(stmt).all())
        if not items:
            # Fallback to any available seeded items in database
            items = list(session.scalars(select(Item).limit(limit)).all())
    return items
