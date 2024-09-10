"""Database data model."""

import uuid

from sqlalchemy import FLOAT, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.data.database import Base


class UsersTableItem(Base):
    """Data model for table to store user data."""

    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    color = Column(String, nullable=False)
    location = Column(String, nullable=False)
    lat = Column(FLOAT(precision=32), nullable=False)
    lon = Column(FLOAT(precision=32), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class ExperiencesTableItem(Base):
    """Data model for table to store user experiences."""

    __tablename__ = "experiences"

    experience_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    lat = Column(FLOAT(precision=32), nullable=False)
    lon = Column(FLOAT(precision=32), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    owner = relationship("UsersTableItem", lazy="subquery")
