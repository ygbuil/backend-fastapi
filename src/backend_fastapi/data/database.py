"""Database module."""

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))  # type: ignore

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db_session() -> Generator[Session]:
    """Create a session with SessionLocal."""
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
