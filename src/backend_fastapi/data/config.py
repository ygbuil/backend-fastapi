"""Database config."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Database settings."""

    db_user: str | None
    db_password: str | None
    db_host: str | None
    db_port: int | None
    db_name: str | None
    secret_key: str | None


settings = Settings(
    db_user=os.getenv("DB_USER"),
    db_password=os.getenv("DB_PASSWORD"),
    db_host=os.getenv("DB_HOST"),
    db_port=int(os.getenv("DB_PORT", "5432")),
    db_name=os.getenv("DB_NAME"),
    secret_key=os.getenv("SECRET_KEY"),
)
