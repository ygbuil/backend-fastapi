"""Module to execute to create the database tables."""

from app.data import Base
from app.database import engine

# create DB
Base.metadata.create_all(bind=engine)
