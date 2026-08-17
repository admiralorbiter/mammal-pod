"""Integration tests for item bank ingestion from disk, SQLite storage, and protocol querying."""

from __future__ import annotations

from pathlib import Path
import pytest
from sqlalchemy.orm import Session

from mammal.items.bank import get_items_for_protocol, import_item_bank_from_disk
from mammal.items.loaders import get_default_item_banks_dir, load_item_banks_from_directory
from mammal.items.validator import ItemValidator
from mammal.models.entities import Item


def test_default_disk_item_banks_valid():
    banks_dir = get_default_item_banks_dir()
    assert banks_dir.exists()

    raw_items = load_item_banks_from_directory(banks_dir)
    assert len(raw_items) >= 400

    validator = ItemValidator()
    report = validator.validate_items(raw_items)
    assert report.is_valid, f"Validation errors found: {[e.message for e in report.errors]}"
    assert report.total_items == report.valid_items
    assert report.invalid_items == 0


def test_import_item_banks_to_database(session: Session):
    banks_dir = get_default_item_banks_dir()
    registered, errors = import_item_bank_from_disk(session, banks_dir)
    assert len(errors) == 0
    assert len(registered) >= 400

    db_items = session.query(Item).all()
    assert len(db_items) >= 400

    # Ensure all registered items have 64-char SHA-256 content hashes
    for item in db_items:
        assert len(item.content_hash) == 64
        assert item.partition in ("engineering", "calibration", "exploratory", "confirmatory", "reserve")


def test_get_items_for_protocol_by_domain_and_partition(session: Session):
    banks_dir = get_default_item_banks_dir()
    import_item_bank_from_disk(session, banks_dir)

    # 1. Query semantic confirmatory items
    sem_conf = get_items_for_protocol(session, domain="semantic", partition="confirmatory", limit=15)
    assert len(sem_conf) == 15
    for item in sem_conf:
        assert item.domain == "semantic"
        assert item.partition == "confirmatory"

    # 2. Query formal exploratory items
    formal_expl = get_items_for_protocol(session, domain="formal", partition="exploratory", limit=10)
    assert len(formal_expl) == 10
    for item in formal_expl:
        assert item.domain in ("formal_math_logic", "formal_code_reasoning")
        assert item.partition == "exploratory"

    # 3. Query future memory calibration items
    mem_calib = get_items_for_protocol(session, domain="future_memory", partition="calibration", limit=10)
    assert len(mem_calib) == 10
    for item in mem_calib:
        assert item.domain == "future_memory"
        assert item.partition == "calibration"

    # 4. Query perceptual RDK items
    rdk_items = get_items_for_protocol(session, domain="perception_rdk", partition="confirmatory", limit=10)
    assert len(rdk_items) == 10
    for item in rdk_items:
        assert item.domain == "perception_rdk"
        assert item.partition == "confirmatory"
