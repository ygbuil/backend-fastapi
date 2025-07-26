"""Schemas for requests and responses."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NewUser(BaseModel):
    """NewExperience schema."""

    username: str
    color: str
    location: str
    lat: float
    lon: float
    password: str


class User(NewUser):
    """NewExperience schema."""

    user_id: UUID
    created_at: datetime


class UserUpdateInfo(BaseModel):
    """UserUpdateInfo schema."""

    user_id: str
    username: str | None
    color: str | None
    location: str | None
    lat: float | None
    lon: float | None
    password: str | None


class NewExperience(BaseModel):
    """NewExperience schema."""

    title: str
    description: str
    location: str
    lat: float
    lon: float
    rating: int


class ExperienceResponse(NewExperience):
    """ExperienceResponse schema."""

    user_id: UUID
    experience_id: UUID
    created_at: datetime
    lifetime: str

    owner: User

    class Config:
        """Config."""

        from_attributes = True


class ExperienceUpdateInfo(BaseModel):
    """ExperienceUpdateInfo schema."""

    experience_id: str
    title: str | None
    description: str | None
    location: str | None
    lat: float | None
    lon: float | None
    rating: int | None


class ExperienceFilters(BaseModel):
    """ExperienceFilters schema."""

    experience_id: str | None
    user_id: str | None
    title: str | None
    description: str | None
    location: str | None
    rating: str | None
    created_at: str | None
