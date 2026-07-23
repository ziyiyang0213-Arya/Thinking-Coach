"""Runtime configuration loaded from environment variables."""

from dataclasses import dataclass
from os import getenv
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    database_path: Path
    openai_model: str
    openai_api_key: str | None

    @classmethod
    def from_environment(cls, database_path: str | None = None) -> "Settings":
        return cls(
            database_path=Path(database_path or getenv("THINKING_COACH_DB", "thinking_coach.db")),
            openai_model=getenv("THINKING_COACH_MODEL", "gpt-4.1-mini"),
            openai_api_key=getenv("OPENAI_API_KEY"),
        )
