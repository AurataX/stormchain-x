import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    database_url: str = field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./stormchain.db")
    )
    operator_token: str = field(default_factory=lambda: os.getenv("OPERATOR_TOKEN", ""))
    gemini_api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    vertex_project: str = field(default_factory=lambda: os.getenv("GOOGLE_CLOUD_PROJECT", ""))
    vertex_location: str = field(default_factory=lambda: os.getenv("GOOGLE_CLOUD_LOCATION", ""))
    vertex_model: str = field(default_factory=lambda: os.getenv("VERTEX_MODEL", "gemini-3.5-flash"))

    def __post_init__(self):
        if not self.database_url.startswith(("sqlite+aiosqlite://", "postgresql+asyncpg://")):
            raise ValueError("Use sqlite+aiosqlite or postgresql+asyncpg")
        if self.operator_token and len(self.operator_token) < 24:
            raise ValueError("OPERATOR_TOKEN requires at least 24 characters")
