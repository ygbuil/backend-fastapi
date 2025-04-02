"""Module to execute to create the database tables."""

from backend_fastapi.data import Base
from backend_fastapi.data.database import engine

# create DB
Base.metadata.create_all(bind=engine)  # type: ignore
