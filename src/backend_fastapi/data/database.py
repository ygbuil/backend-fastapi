"""Database module."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

# create engine to interact with DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create class to create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# used to define DB architecture
Base = declarative_base()

# create DB
Base.metadata.create_all(bind=engine)  # type: ignore


def get_db_session() -> Generator[Session]:
    """Create a session with SessionLocal."""
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
