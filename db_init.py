"""Module to execute to create the database tables."""

from app.database import engine
from app.models import Base

# create DB
Base.metadata.create_all(bind=engine)
