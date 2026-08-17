"""Configuration and path management for Project MAMMAL."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for Project MAMMAL."""

    data_root: Path
    db_path: Path
    db_url: str

    @classmethod
    def load(cls, custom_data_root: str | Path | None = None) -> Settings:
        """Load settings from environment variable MAMMAL_DATA_ROOT or custom path."""
        if custom_data_root is not None:
            root = Path(custom_data_root).expanduser().resolve()
        else:
            env_root = os.getenv("MAMMAL_DATA_ROOT")
            if env_root:
                root = Path(env_root).expanduser().resolve()
            else:
                root = Path.home() / ".mammal-pod" / "data"

        db_path = root / "database" / "mammal.db"
        # On Windows, path must be properly formatted for SQLite URL (sqlite:///C:/path...)
        db_url = f"sqlite:///{db_path.as_posix()}"

        return cls(
            data_root=root,
            db_path=db_path,
            db_url=db_url,
        )

    def ensure_directories(self) -> None:
        """Ensure standard data root directory layout exists."""
        subdirectories = [
            self.data_root / "raw" / "audio",
            self.data_root / "raw" / "protocol_snapshots",
            self.data_root / "raw" / "observer_outputs",
            self.data_root / "derived" / "wav",
            self.data_root / "derived" / "transcripts",
            self.data_root / "derived" / "acoustic_features",
            self.data_root / "derived" / "reports",
            self.data_root / "exports" / "private",
            self.data_root / "exports" / "analysis",
            self.data_root / "exports" / "public",
            self.data_root / "database",
            self.data_root / "backups",
        ]
        for directory in subdirectories:
            directory.mkdir(parents=True, exist_ok=True)


# Global default settings instance
settings = Settings.load()
