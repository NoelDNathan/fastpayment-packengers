"""Application configuration using Pydantic Settings v2."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Environment
    environment: str = "development"
    debug: bool = True

    # Database (required - must be set in .env)
    database_url: str

    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # Prometheus
    prometheus_enabled: bool = False

    # Logging
    log_level: str = "DEBUG"

    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
