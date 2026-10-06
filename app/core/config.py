import secrets

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    DATABASE_URL can later be changed to a PostgreSQL URL for Azure.
    SECRET_KEY is generated automatically for local development if it
    is not provided. Production deployments should always provide it
    through an environment variable.
    """

    database_url: str = "sqlite:///./task_management.db"

    secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        min_length=32,
    )

    access_token_expire_minutes: int = Field(
        default=30,
        ge=1,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
