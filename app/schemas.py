from datetime import datetime
from typing import Optional
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


class UserResponse(BaseModel):
    """NewExperience data model."""

    user_id: UUID
    username: str
    color: str
    location: str
    lat: float
    lon: float
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdateInfo(BaseModel):
    """UserUpdateInfo schema."""

    user_id: str
    username: Optional[str]
    color: Optional[str]
    location: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    password: Optional[str]


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

    owner: UserResponse

    class Config:
        from_attributes = True


class ExperienceUpdateInfo(BaseModel):
    """ExperienceUpdateInfo schema."""

    experience_id: str
    title: Optional[str]
    description: Optional[str]
    location: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    rating: Optional[int]


class ExperienceFilters(BaseModel):
    """ExperienceFilters schema."""

    experience_id: Optional[str]
    user_id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    location: Optional[str]
    rating: Optional[str]
    created_at: Optional[str]
