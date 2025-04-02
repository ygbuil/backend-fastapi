"""Experiences endpoints."""

import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend_fastapi import data, endpoint_functions
from backend_fastapi.data import (
    ExperienceResponse,
    ExperiencesTableItem,
    ExperienceUpdateInfo,
    NewExperience,
    UsersTableItem,
)

experiences_router = APIRouter(prefix="/experiences")


@experiences_router.post("", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
def create_experience(
    experience_to_create: NewExperience,
    verified_user: Annotated[UsersTableItem, Depends(endpoint_functions.get_verified_user)],
    db_session: Annotated[Session, Depends(data.get_db_session)],
) -> ExperiencesTableItem:
    """Create new experience."""
    created_experience = endpoint_functions.create_experience(
        db_session=db_session,
        verified_user=verified_user,
        experience_to_create=experience_to_create,
    )
    return _add_lifetime_to_experience(
        experience=created_experience,
        created_at=created_experience.created_at,  # type: ignore
    )


@experiences_router.get("/{experience_id}", response_model=ExperienceResponse)
def get_experience(
    experience_id: str,
    db_session: Annotated[Session, Depends(data.get_db_session)],
) -> ExperiencesTableItem:
    """Get experience based on id."""
    experience = endpoint_functions.get_experience_by_id(
        db_session=db_session,
        experience_id=experience_id,
    )

    if experience is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")

    return _add_lifetime_to_experience(
        experience=experience,
        created_at=experience.created_at,  # type: ignore
    )


@experiences_router.get("", response_model=list[ExperienceResponse])
def get_experience_by_filter(
    db_session: Annotated[Session, Depends(data.get_db_session)],
    limit: int = 10,
    skip: int = 0,
    experience: str | None = "",
    title: str | None = "",
    description: str | None = "",
    location: str | None = "",
    user: str | None = None,
    rating: int | None = None,
) -> list[ExperiencesTableItem]:
    """Filter experiences by matching string in specific field."""
    filtered_experiences = endpoint_functions.get_experience_by_filters(
        db_session=db_session,
        limit=limit,
        skip=skip,
        experience=experience,
        title=title,
        description=description,
        location=location,
        user=user,
        rating=rating,
    )

    if filtered_experiences is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiences not found")

    return [
        _add_lifetime_to_experience(
            experience=filtered_experience,
            created_at=filtered_experience.created_at,  # type: ignore
        )
        for filtered_experience in filtered_experiences
    ]


@experiences_router.put("/{experience_id}", response_model=ExperienceResponse)
def update_experience(
    experience_update_info: ExperienceUpdateInfo,
    verified_user: Annotated[UsersTableItem, Depends(endpoint_functions.get_verified_user)],
    db_session: Annotated[Session, Depends(data.get_db_session)],
) -> ExperiencesTableItem:
    """Update experience content."""
    experience = endpoint_functions.get_experience_by_id(
        db_session=db_session,
        experience_id=experience_update_info.experience_id,
    )

    if experience is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")

    if str(verified_user.user_id) != str(experience.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    updated_experience = endpoint_functions.update_experience(
        db_session=db_session,
        experience=experience,
        experience_update_info=experience_update_info,
    )

    return _add_lifetime_to_experience(
        experience=updated_experience,
        created_at=updated_experience.created_at,  # type: ignore
    )


@experiences_router.delete("/{experience_id}", response_model=ExperienceResponse)
def delete_experience(
    experience_id: str,
    verified_user: Annotated[UsersTableItem, Depends(endpoint_functions.get_verified_user)],
    db_session: Annotated[Session, Depends(data.get_db_session)],
) -> ExperiencesTableItem:
    """Delete experience by id."""
    experience = endpoint_functions.get_experience_by_id(
        db_session=db_session,
        experience_id=experience_id,
    )

    if experience is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")

    if str(verified_user.user_id) != str(experience.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    deleted_experience = endpoint_functions.delete_experience(
        db_session=db_session,
        experience=experience,
    )

    return _add_lifetime_to_experience(
        experience=deleted_experience,
        created_at=deleted_experience.created_at,  # type: ignore
    )


def _add_lifetime_to_experience(
    experience: ExperiencesTableItem, created_at: datetime.datetime
) -> ExperiencesTableItem:
    """Calculate the time that happened since a experience was created."""
    days_dif = (datetime.datetime.now(tz=datetime.UTC) - created_at).days

    years = days_dif // 365
    weeks = int((days_dif % 365) / 7)
    days = int((days_dif % 365) % 7)

    lifetime = ""

    if years != 0:
        lifetime += str(years) + "y, "
    if weeks != 0:
        lifetime += str(weeks) + "w, "
    if days != 0:
        lifetime += str(days) + "d, "

    lifetime = "today" if lifetime == "" else lifetime[:-2] + " ago"
    experience.lifetime = lifetime

    return experience
