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
        existing.prompt_json = item_data["prompt"]
        existing.options_json = item_data.get("options")
        existing.ground_truth_json = item_data["ground_truth"]
        existing.domain = item_data["domain"]
        existing.family = item_data["family"]
        existing.content_hash = content_hash
        session.flush()
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


def generate_rdk_items() -> list[dict[str, Any]]:
    """Generate deterministic Random Dot Kinematogram motion items."""
    items = []
    directions = ["left", "right", "right", "left", "left", "right", "left", "right", "left", "right", "left", "right", "left", "right", "left", "right", "left", "right", "left", "right"]
    coherences = [0.50, 0.40, 0.35, 0.45, 0.30, 0.55, 0.40, 0.50, 0.35, 0.45, 0.50, 0.40, 0.35, 0.45, 0.30, 0.55, 0.40, 0.50, 0.35, 0.45]
    for i, (d, c) in enumerate(zip(directions, coherences), start=1):
        items.append({
            "item_id": f"rdk_motion_{i:03d}",
            "version": "1.0.0",
            "domain": "perception_rdk",
            "family": "motion_discrimination",
            "prompt": {"question": "Discriminate perceived direction of coherent motion", "coherence": c, "direction": d},
            "options": ["left", "right"],
            "ground_truth": {"canonical": d, "option_index": 0 if d == "left" else 1},
            "partition": "engineering",
            "source": {"provenance": "synthetic_rdk_fixtures", "license": "CC0"},
        })
    return items


def generate_memory_items() -> list[dict[str, Any]]:
    """Generate paired associate memory items for prospective JOL protocols."""
    pairs_data = [
        ("adui", "enemy", ["Enemy", "Friend", "Warrior", "Shadow"]),
        ("chakula", "food", ["Food", "Water", "Feast", "Harvest"]),
        ("mwezi", "moon", ["Moon", "Sun", "Sky", "Night"]),
        ("safari", "journey", ["Journey", "Camp", "Trail", "Hunter"]),
        ("samaki", "fish", ["Fish", "River", "Boat", "Net"]),
        ("nyota", "star", ["Star", "Cloud", "Comet", "Spark"]),
        ("ndege", "bird", ["Bird", "Wing", "Wind", "Nest"]),
        ("kitabu", "book", ["Book", "Letter", "Scroll", "Story"]),
        ("barabara", "road", ["Road", "Bridge", "Path", "Mountain"]),
        ("maji", "water", ["Water", "Ocean", "Rain", "River"]),
    ]
    items = []
    for i, (cue, target, options) in enumerate(pairs_data, start=1):
        items.append({
            "item_id": f"mem_pair_{i:03d}",
            "version": "1.0.0",
            "domain": "future_memory",
            "family": "cued_recall_jol",
            "prompt": {
                "cue": cue.upper(),
                "target": target.upper(),
                "study_text": f"{cue.upper()} \u2192 {target.upper()}",
                "test_question": f"What is the English translation for '{cue.upper()}'?",
            },
            "options": options,
            "ground_truth": {"canonical": target, "option_index": 0},
            "partition": "engineering",
            "source": {"provenance": "swahili_english_associates_v1", "license": "CC0"},
        })
    return items


def seed_qualification_items(session: Session) -> list[Item]:
    """Ensure baseline qualification items (100 items) are present in item bank."""
    from mammal.items.qualification import generate_e00_qualification_items
    all_fixtures = QUALIFICATION_FIXTURE_ITEMS + generate_e00_qualification_items() + generate_rdk_items() + generate_memory_items()
    registered = []
    for item_dict in all_fixtures:
        item = register_item(session, item_dict)
        registered.append(item)
    return registered


def get_items_for_protocol(
    session: Session,
    domain: str | None = None,
    partition: str = "engineering",
    limit: int = 10,
) -> Sequence[Item]:
    """Query available items for an experiment partition and domain."""
    if domain in ("perception_rdk", "perceptual_psychophysics"):
        query = select(Item).where(Item.domain == "perception_rdk").limit(limit)
        items = list(session.scalars(query).all())
        if not items:
            seed_qualification_items(session)
            items = list(session.scalars(query).all())
        return items

    if domain == "future_memory":
        query = select(Item).where(Item.domain == "future_memory").limit(limit)
        items = list(session.scalars(query).all())
        if not items:
            seed_qualification_items(session)
            items = list(session.scalars(query).all())
        return items

    # Standard protocols: query by partition, fallback to any non-rdk items
    query = select(Item).where(Item.partition == partition).limit(limit)
    items = list(session.scalars(query).all())
    if not items:
        seed_qualification_items(session)
        items = list(session.scalars(query).all())
    if not items:
        items = list(session.scalars(select(Item).where(Item.domain != "perception_rdk").limit(limit)).all())
    return items
