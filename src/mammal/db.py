"""Database engine, connection lifecycle, and transaction management."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import Engine, create_engine, event, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from mammal.config import Settings, settings

Base = declarative_base()


def configure_sqlite_pragmas(dbapi_connection, connection_record) -> None:
    """Ensure SQLite enforces foreign key constraints and runs in WAL mode."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.close()


def create_db_engine(db_url: str | None = None) -> Engine:
    """Create a configured SQLAlchemy engine for SQLite."""
    url = db_url or settings.db_url
    engine = create_engine(url, echo=False, future=True)
    event.listen(engine, "connect", configure_sqlite_pragmas)
    return engine


_engine: Engine | None = None
_SessionFactory: sessionmaker[Session] | None = None


def get_engine(app_settings: Settings | None = None) -> Engine:
    """Get or initialize the global database engine."""
    global _engine, _SessionFactory
    if _engine is None:
        target_settings = app_settings or settings
        target_settings.ensure_directories()
        _engine = create_db_engine(target_settings.db_url)
        _SessionFactory = sessionmaker(bind=_engine, autocommit=False, autoflush=False, future=True)
    return _engine


def get_session_factory(app_settings: Settings | None = None) -> sessionmaker[Session]:
    """Get the sessionmaker factory."""
    global _SessionFactory
    if _SessionFactory is None:
        get_engine(app_settings)
    assert _SessionFactory is not None
    return _SessionFactory


@contextmanager
def get_session(app_settings: Settings | None = None) -> Generator[Session, None, None]:
    """Provide a transactional database session context."""
    factory = get_session_factory(app_settings)
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db(engine: Engine | None = None, app_settings: Settings | None = None) -> None:
    """Create all tables in the database."""
    target_engine = engine or get_engine(app_settings)
    Base.metadata.create_all(bind=target_engine)


def check_db(engine: Engine | None = None, app_settings: Settings | None = None) -> dict[str, str]:
    """Check database health, foreign keys, and integrity."""
    target_engine = engine or get_engine(app_settings)
    with target_engine.connect() as conn:
        fk_result = conn.execute(text("PRAGMA foreign_keys;")).scalar()
        wal_result = conn.execute(text("PRAGMA journal_mode;")).scalar()
        integrity_result = conn.execute(text("PRAGMA integrity_check;")).scalar()

    return {
        "foreign_keys": "ON" if fk_result == 1 else "OFF",
        "journal_mode": str(wal_result).upper(),
        "integrity": str(integrity_result),
    }
