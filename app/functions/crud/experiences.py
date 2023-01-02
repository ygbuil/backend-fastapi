# libraries
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

# local libraries
from app.models import ExperiencesTableItem, UsersTableItem
from app.schemas import NewExperience, ExperienceUpdateInfo, User


def get_experience_by_id(db_session: Session, experience_id: str):
    statement = (
        db_session.query(ExperiencesTableItem)
        .filter(ExperiencesTableItem.experience_id == experience_id)
    )

    return statement.first()


def get_experience_by_filters(
    db_session: Session, limit: int, skip: int, experience:str, title: str,
    description: str, location: str, user: str, rating: int
):
    experiences = (
        db_session.query(ExperiencesTableItem).filter(
            *([ExperiencesTableItem.title.contains(title)] if title else []
              + [ExperiencesTableItem.description.contains(description)] \
                if description else []
              + [or_(ExperiencesTableItem.description.contains(experience),
                ExperiencesTableItem.title.contains(experience))] \
                if experience else []
              + [ExperiencesTableItem.location.contains(location)] \
                if location else []
              + [ExperiencesTableItem.owner.has(
                    UsersTableItem.username.contains(user)
                )] if user else []
              + [ExperiencesTableItem.rating == rating] if rating else []
             )
        )
        .order_by(ExperiencesTableItem.created_at.desc()).limit(limit)
        .offset(skip).all()
    )
    
    return experiences


def create_experience(
    db_session: Session, verified_user: User,
    experience_to_create: NewExperience
):
    experience = ExperiencesTableItem(
        user_id=str(verified_user.user_id), **experience_to_create.dict()
    )
    
    try:
        db_session.add(experience)
        db_session.commit()
        db_session.refresh(experience)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request'
        )

    return experience


def update_experience(
    db_session: Session, experience_update_info: ExperienceUpdateInfo
):
    experience = get_experience_by_id(
        db_session=db_session,
        experience_id=experience_update_info.experience_id
    )
    
    for key, value in experience_update_info.dict().items():
        if value is not None:
            setattr(experience, key, value)

    db_session.commit()
    db_session.refresh(experience)

    return experience


def delete_experience(db_session: Session, experience_id: str):
    experience = get_experience_by_id(
        db_session=db_session, experience_id=experience_id
    )
    
    db_session.delete(experience)
    db_session.commit()
    
    return experience
