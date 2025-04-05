"""Module to create database tables."""

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from backend_fastapi import data
from backend_fastapi.entry_points import app

engine = create_engine(os.getenv("DATABASE_URL_TEST"))  # type: ignore

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def override_get_db_session() -> Generator[Session]:
    """Create a session with SessionLocal."""
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


app.dependency_overrides[data.get_db_session] = override_get_db_session
