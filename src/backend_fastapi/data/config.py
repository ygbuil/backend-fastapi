"""Database config."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Database settings."""

    secret_key: str | None


settings = Settings(
    secret_key=os.getenv("SECRET_KEY"),
)
