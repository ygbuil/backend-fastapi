# libraries
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# users
class NewUser(BaseModel):
    username: str
    color: str
    location: str
    lat: float
    lon: float
    password: str


class User(NewUser):
    user_id: UUID
    created_at: datetime


class UserResponse(BaseModel):
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
    user_id: str
    username: Optional[str]
    color: Optional[str]
    location: Optional[str]
    lat: Optional[str]
    lon: Optional[str]
    password: Optional[str]


# experiences
class NewExperience(BaseModel):
    title: str
    description: str
    location: str
    lat: float
    lon: float
    rating: int


class ExperienceResponse(NewExperience):
    user_id: UUID
    experience_id: UUID
    created_at: datetime
    lifetime: str

    owner: UserResponse

    class Config:
        from_attributes = True


class ExperienceUpdateInfo(BaseModel):
    experience_id: str
    title: Optional[str]
    description: Optional[str]
    location: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    rating: Optional[int]


class ExperienceFilters(BaseModel):
    experience_id: Optional[str]
    user_id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    location: Optional[str]
    rating: Optional[str]
    created_at: Optional[str]
