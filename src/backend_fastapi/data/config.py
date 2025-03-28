"""Database config."""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Database settings."""

    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    secret_key: str

    class Config:
        """Config."""

        env_file = Path.cwd() / Path(".env")


settings = Settings()
