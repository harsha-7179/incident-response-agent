"""Central config: every setting is read from the project-root .env file."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")

    shoplite_database_url: str
    dejavu_database_url: str

    hindsight_api_key: str = ""
    hindsight_base_url: str = ""

    gemini_api_key: str = ""
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    gemini_model: str = "gemini-3.5-flash-lite"
    gemini_fallback_models: str = "gemini-3.1-flash-lite"  # comma-separated, tried in order

    shoplite_url: str = "http://localhost:8001"
    log_dir: str = "logs"

    @property
    def gemini_models(self) -> list[str]:
        """Main model first, then each fallback in order (deduplicated)."""
        names = [self.gemini_model, *self.gemini_fallback_models.split(",")]
        return list(dict.fromkeys(n.strip() for n in names if n.strip()))

    @property
    def log_path(self) -> Path:
        path = Path(self.log_dir)
        return path if path.is_absolute() else ROOT_DIR / path


@lru_cache
def get_settings() -> Settings:
    return Settings()
