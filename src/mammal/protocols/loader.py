"""Protocol loader, schema validator, and database registrar."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft202012Validator
import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session

from mammal.models.entities import Protocol


def get_protocol_schema() -> dict[str, Any]:
    """Load JSON schema for Project MAMMAL protocols."""
    schema_path = Path(__file__).resolve().parents[3] / "schemas" / "protocol.schema.json"
    if not schema_path.exists():
        # Fallback to current working directory
        schema_path = Path("schemas") / "protocol.schema.json"
    return json.loads(schema_path.read_text(encoding="utf-8"))


def load_protocol_file(file_path: str | Path) -> dict[str, Any]:
    """Read and validate a protocol YAML file against its JSON schema."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Protocol file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML content in {path}: expected dictionary root.")

    schema = get_protocol_schema()
    validator = Draft202012Validator(schema)
    validator.validate(data)
    return data


def register_protocol(session: Session, protocol_data: dict[str, Any]) -> Protocol:
    """Register or update a protocol configuration in the database."""
    pid = protocol_data["protocol_id"]
    version = str(protocol_data["version"])

    stmt = select(Protocol).where(Protocol.protocol_id == pid, Protocol.version == version)
    existing = session.scalars(stmt).first()

    if existing:
        existing.domain = protocol_data["domain"]
        existing.mode = protocol_data["mode"]
        existing.status = protocol_data.get("status", "engineering")
        existing.schema_json = protocol_data
        session.flush()
        return existing

    protocol = Protocol(
        protocol_id=pid,
        version=version,
        domain=protocol_data["domain"],
        mode=protocol_data["mode"],
        status=protocol_data.get("status", "engineering"),
        schema_json=protocol_data,
    )
    session.add(protocol)
    session.flush()
    return protocol


def load_and_register_all_protocols(session: Session, config_dir: str | Path | None = None) -> list[Protocol]:
    """Scan and register all YAML protocols in config directory."""
    if config_dir is None:
        target_dir = Path(__file__).resolve().parents[3] / "config"
        if not target_dir.exists():
            target_dir = Path("config")
    else:
        target_dir = Path(config_dir)

    registered = []
    for yaml_file in target_dir.glob("*.yaml"):
        # Skip non-protocol configs like observer configs
        try:
            data = load_protocol_file(yaml_file)
            proto = register_protocol(session, data)
            registered.append(proto)
        except (ValidationError, KeyError):
            # Not a protocol file
            continue

    return registered
