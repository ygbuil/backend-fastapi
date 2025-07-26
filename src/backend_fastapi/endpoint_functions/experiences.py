"""Funtions that deal with experiences."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend_fastapi.data import (
    ExistingUser,
    ExperiencesTableItem,
    ExperienceUpdateInfo,
    NewExperience,
    UsersTableItem,
)


def get_experience_by_id(db_session: Session, experience_id: str) -> ExperiencesTableItem | None:
    """Get experience based on provided experience_id."""
    return (
        db_session.query(ExperiencesTableItem)
        .filter(
            ExperiencesTableItem.experience_id == experience_id,
        )
        .first()
    )


def get_experience_by_filters(
    db_session: Session,
    limit: int | None,
    skip: int | None,
    title: str | None,
    description: str | None,
    location: str | None,
    user: str | None,
    rating: int | None,
) -> list[ExperiencesTableItem]:
    """Get experience based on keywords for each filed."""
    filters = []
    if title:
        filters.append(ExperiencesTableItem.title.contains(title))
    if description:
        filters.append(ExperiencesTableItem.description.contains(description))
    if location:
        filters.append(ExperiencesTableItem.location.contains(location))
    if user:
        filters.append(ExperiencesTableItem.owner.has(UsersTableItem.username.contains(user)))
    if rating is not None:
        filters.append(ExperiencesTableItem.rating == rating)

    return (
        db_session.query(ExperiencesTableItem)
        .filter(*filters)
        .order_by(ExperiencesTableItem.created_at.desc())
        .limit(limit)
        .offset(skip)
        .all()
    )


def create_experience(
    db_session: Session,
    verified_user: ExistingUser,
    experience_to_create: NewExperience,
) -> ExperiencesTableItem:
    """Create a new experience."""
    experience = ExperiencesTableItem(
        user_id=str(verified_user.user_id),
        **experience_to_create.model_dump(),
    )

    try:
        db_session.add(experience)
        db_session.commit()
        db_session.refresh(experience)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request") from exc

    return experience


def update_experience(
    db_session: Session,
    experience: ExperiencesTableItem,
    experience_update_info: ExperienceUpdateInfo,
) -> ExperiencesTableItem:
    """Update values of an experience."""
    for key, value in experience_update_info.model_dump().items():
        if value is not None:
            setattr(experience, key, value)

    db_session.commit()
    db_session.refresh(experience)

    return experience


def delete_experience(
    db_session: Session, experience: ExperiencesTableItem
) -> ExperiencesTableItem:
    """Delete experience."""
    db_session.delete(experience)
    db_session.commit()

    return experience
