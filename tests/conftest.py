from __future__ import annotations

try:
    import six
    if hasattr(six, "_SixMetaPathImporter") and not hasattr(six._SixMetaPathImporter, "_path"):
        six._SixMetaPathImporter._path = None
except ImportError:
    pass

from pathlib import Path
from typing import Generator

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from mammal.artifacts.store import ArtifactStore
from mammal.config import Settings
from mammal.db import Base, create_db_engine, init_db


@pytest.fixture
def temp_settings(tmp_path: Path) -> Settings:
    """Create isolated settings with temporary data root."""
    settings = Settings.load(custom_data_root=tmp_path / "mammal_test_data")
    settings.ensure_directories()
    return settings


@pytest.fixture
def engine(temp_settings: Settings) -> Engine:
    """Create a clean database engine with tables created."""
    engine = create_db_engine(temp_settings.db_url)
    init_db(engine)
    return engine


@pytest.fixture
def session(engine: Engine) -> Generator[Session, None, None]:
    """Provide an isolated database session for testing."""
    factory = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
    sess = factory()
    try:
        yield sess
        sess.commit()
    except Exception:
        sess.rollback()
        raise
    finally:
        sess.close()


@pytest.fixture
def artifact_store(temp_settings: Settings) -> ArtifactStore:
    """Provide an ArtifactStore operating within temporary directory."""
    return ArtifactStore(temp_settings)
