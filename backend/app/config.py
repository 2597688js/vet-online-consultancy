import secrets
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BACKEND_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    # Default: a local Postgres, connecting as the current OS user (Homebrew / Postgres.app default).
    database_url: str = "postgresql+psycopg://localhost:5432/vet_online_consultancy"
    # Signs login tokens. Generated and saved to backend/.env on first run if not set.
    jwt_secret: str = ""
    # The doctor's email: receives appointment reminder emails.
    doctor_email: str = ""
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    cors_origins: str = "http://localhost:5173"
    google_client_id: str = ""
    upload_dir: str = "uploads"
    max_upload_mb: int = 5
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    app_base_url: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


def _ensure_secret(settings: Settings, field: str, generate) -> None:
    """Generate a missing secret once and save it to backend/.env so it survives restarts."""
    if getattr(settings, field):
        return
    value = generate()
    setattr(settings, field, value)
    existing = ENV_FILE.read_text() if ENV_FILE.exists() else ""
    separator = "" if not existing or existing.endswith("\n") else "\n"
    ENV_FILE.write_text(f"{existing}{separator}{field.upper()}={value}\n")


settings = Settings()
_ensure_secret(settings, "jwt_secret", lambda: secrets.token_hex(32))
