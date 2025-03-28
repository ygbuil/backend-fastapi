"""Module to create database tables."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from backend_fastapi import data
from backend_fastapi.data import settings
from backend_fastapi.entry_points import app

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}_test"
)

# create engine to interact with DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create class to create session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# used to define DB architecture
Base = declarative_base()

# create DB
Base.metadata.create_all(bind=engine)


def override_get_db_session() -> Generator[Session]:
    """Create a session with SessionLocal."""
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


app.dependency_overrides[data.get_db_session] = override_get_db_session
