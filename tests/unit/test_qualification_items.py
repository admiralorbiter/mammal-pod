"""Unit tests for 100-item E00 qualification fixture generator and schema conformance."""

from __future__ import annotations

import pytest
from jsonschema.validators import Draft202012Validator
from sqlalchemy.orm import Session

from mammal.items.bank import get_item_schema, seed_qualification_items
from mammal.items.qualification import generate_e00_qualification_items
from mammal.models.entities import Item


def test_generate_100_qualification_items():
    items = generate_e00_qualification_items()
    assert len(items) == 100

    schema = get_item_schema()
    validator = Draft202012Validator(schema)

    item_ids = set()
    for item in items:
        # 1. Conforms to item.schema.json
        validator.validate(item)

        # 2. Unique item IDs
        assert item["item_id"] not in item_ids
        item_ids.add(item["item_id"])

        # 3. Valid options and ground truth
        options = item["options"]
        gt = item["ground_truth"]
        assert len(options) >= 2
        assert gt["canonical"] in options
        assert options[gt["option_index"]] == gt["canonical"]


def test_seed_e00_qualification_items_in_database(session: Session):
    registered = seed_qualification_items(session)
    session.commit()

    assert len(registered) >= 100
    db_items = session.query(Item).all()
    assert len(db_items) >= 100

    # Ensure all items have valid computed content hashes
    for itm in db_items:
        assert len(itm.content_hash) == 64  # SHA-256 hex length
