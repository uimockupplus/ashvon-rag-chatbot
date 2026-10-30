"""Centralized, typed application settings.

All machine-specific paths and model names are configurable through environment
variables or a local .env file. No credentials are required by this project.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """Runtime settings for the offline Ashvon RAG application."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Ashvon Technologies RAG Chatbot"
    app_env: str = "development"
    log_level: str = "INFO"

    ollama_host: str = "http://localhost:11434"
    ollama_chat_model: str = "ashvon-qwen2.5"
    ollama_embedding_model: str = "nomic-embed-text"

    chroma_persist_directory: str = "./data/chroma_db"
    chroma_collection_name: str = "ashvon_website"

    top_k: Annotated[int, Field(ge=1, le=20)] = 5
    chunk_size: Annotated[int, Field(ge=100, le=2000)] = 400
    chunk_overlap: Annotated[int, Field(ge=0, le=500)] = 70
    max_distance: Annotated[float, Field(ge=0.0, le=2.0)] = 0.75

    request_timeout: Annotated[int, Field(ge=1, le=120)] = 20
    crawl_user_agent: str = "AshvonTechnologiesKnowledgeBot/1.0"
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://ashvontech.com",
    ]

    @field_validator("ollama_host")
    @classmethod
    def normalize_ollama_host(cls, value: str) -> str:
        """Remove a trailing slash to avoid malformed endpoint URLs."""
        return value.rstrip("/")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}:
            raise ValueError("LOG_LEVEL must be a valid Python logging level.")
        return normalized

    @property
    def chroma_path(self) -> Path:
        """Resolve relative Chroma paths against the project root."""
        path = Path(self.chroma_persist_directory).expanduser()
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path.resolve()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return one cached settings instance for the application process."""
    return Settings()


def configure_logging() -> None:
    """Configure consistent application logging from environment settings."""
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


settings = get_settings()
configure_logging()
logger = logging.getLogger("ashvon_rag")
