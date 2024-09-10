"""Experiences endpoints."""

import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app import database, endpoint_functions
from app.data import ExperienceResponse, ExperiencesTableItem, ExperienceUpdateInfo, NewExperience

experiences_router = APIRouter(prefix="/experiences")


@experiences_router.post("", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
def create_experience(
    experience_to_create: NewExperience,
    verified_user: Depends = Depends(endpoint_functions.get_verified_user),  # noqa: B008
    db_session: Depends = Depends(database.get_db_session),  # noqa: B008
) -> ExperiencesTableItem:
    """Create new experience."""
    created_experience = endpoint_functions.create_experience(
        db_session=db_session,
        verified_user=verified_user,
        experience_to_create=experience_to_create,
    )
    return _add_lifetime_to_experience(
        experience=created_experience,
        created_at=created_experience.created_at,
    )


@experiences_router.get("/{experience_id}", response_model=ExperienceResponse)
def get_experience(
    experience_id: str,
    db_session: Depends = Depends(database.get_db_session),  # noqa: B008
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
        created_at=experience.created_at,
    )


@experiences_router.get("", response_model=List[ExperienceResponse])
def get_experience_by_filter(
    limit: int = 10,
    skip: int = 0,
    experience: Optional[str] = "",
    title: Optional[str] = "",
    description: Optional[str] = "",
    location: Optional[str] = "",
    user: Optional[str] = None,
    rating: Optional[int] = None,
    db_session: Depends = Depends(database.get_db_session),  # noqa: B008
) -> list:
    """Filter experiences by matching string in specific field."""
    experiences_filtered = endpoint_functions.get_experience_by_filters(
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

    if experiences_filtered is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiences not found")

    for idx, experience in enumerate(experiences_filtered):
        experience = _add_lifetime_to_experience(
            experience=experience,
            created_at=experience.created_at,
        )
        experiences_filtered[idx] = experience

    return experiences_filtered


@experiences_router.put("/{experience_id}", response_model=ExperienceResponse)
def update_experience(
    experience_update_info: ExperienceUpdateInfo,
    verified_user: Depends = Depends(endpoint_functions.get_verified_user),  # noqa: B008
    db_session: Depends = Depends(database.get_db_session),  # noqa: B008
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
        experience_update_info=experience_update_info,
    )

    return _add_lifetime_to_experience(
        experience=updated_experience,
        created_at=updated_experience.created_at,
    )


@experiences_router.delete("/{experience_id}", response_model=ExperienceResponse)
def delete_experience(
    experience_id: str,
    verified_user: Depends = Depends(endpoint_functions.get_verified_user),  # noqa: B008
    db_session: Depends = Depends(database.get_db_session),  # noqa: B008
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
        experience_id=experience_id,
    )

    return _add_lifetime_to_experience(
        experience=deleted_experience,
        created_at=deleted_experience.created_at,
    )


def _add_lifetime_to_experience(experience: ExperiencesTableItem, created_at: datetime) -> str:
    """Calculate the time that happened since a experience was created."""
    days_dif = (datetime.datetime.now(tz=datetime.timezone.utc) - created_at).days

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
