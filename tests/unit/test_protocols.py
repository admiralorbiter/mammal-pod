"""Unit tests for protocol loading and schema validation."""

from __future__ import annotations

from pathlib import Path
import pytest
from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft202012Validator
from sqlalchemy.orm import Session

from mammal.protocols.loader import (
    load_and_register_all_protocols,
    load_protocol_file,
    register_protocol,
)


def test_load_e00_qualification_protocol():
    proto_path = Path("config") / "e00_instrument_qualification.yaml"
    data = load_protocol_file(proto_path)
    assert data["protocol_id"] == "e00_instrument_qualification"
    assert data["status"] == "engineering"
    assert data["domain"] == "semantic"
    assert data["answer"]["lock_required"] is True
    assert data["confidence"]["shown_after_answer_lock"] is True


def test_load_e01_semantic_protocol():
    proto_path = Path("config") / "e01_semantic_self.yaml"
    data = load_protocol_file(proto_path)
    assert data["protocol_id"] == "e01_semantic_self"
    assert data["status"] == "exploratory"
    assert data["domain"] == "semantic"


def test_register_protocol_in_db(session: Session):
    proto_path = Path("config") / "e00_instrument_qualification.yaml"
    data = load_protocol_file(proto_path)
    proto_entity = register_protocol(session, data)
    session.commit()

    assert proto_entity.protocol_id == "e00_instrument_qualification"
    assert proto_entity.domain == "semantic"
    assert proto_entity.schema_json["domain"] == "semantic"


def test_invalid_protocol_fails_validation():
    invalid_data = {
        "protocol_id": "bad_proto",
        # Missing required fields like version, status, domain, mode, answer, confidence, feedback, item_bank, analysis
    }
    with pytest.raises(ValidationError):
        from mammal.protocols.loader import get_protocol_schema
        schema = get_protocol_schema()
        Draft202012Validator(schema).validate(invalid_data)
