# libraries
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

# local libraries
from app import oauth2
from app import database
from app.functions import utils
from app.functions.crud import experiences
from app.schemas import (
    ExperienceResponse, NewExperience, ExperienceUpdateInfo
)


experiences_router = APIRouter(prefix='/experiences')


@experiences_router.post(
    '', response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED
)
def create_experience(
    experience_to_create: NewExperience,
    verified_user: int = Depends(oauth2.get_verified_user),
    db_session=Depends(database.get_db_session)
):
    
    created_experience = experiences.create_experience(
        db_session=db_session, verified_user=verified_user,
        experience_to_create=experience_to_create
    )
    created_experience = utils.add_lifetime_to_experience(
        experience=created_experience, created_at=created_experience.created_at
    )

    return created_experience


@experiences_router.get('/{experience_id}', response_model=ExperienceResponse)
def get_experience(
    experience_id: str, db_session=Depends(database.get_db_session)
):
    experience = experiences.get_experience_by_id(
        db_session=db_session, experience_id=experience_id
    )

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Experience not found'
        )

    experience = utils.add_lifetime_to_experience(
        experience=experience, created_at=experience.created_at
    )

    return experience


@experiences_router.get('', response_model=List[ExperienceResponse])
def get_experience_by_filter(
    limit: int = 10, skip: int = 0, title: Optional[str] = '', 
    description: Optional[str] = '', location: Optional[str] = '',
    rating: Optional[int] = None, db_session=Depends(database.get_db_session)
):
    experiences_filtered = experiences.get_experience_by_filters(
        db_session=db_session, limit=limit, skip=skip, title=title,
        description=description, location=location, rating=rating
    )

    if experiences_filtered is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Experiences not found'
        )

    for idx, experience in enumerate(experiences_filtered):
        experience = utils.add_lifetime_to_experience(
            experience=experience, created_at=experience.created_at
        )
        experiences_filtered[idx] = experience

    return experiences_filtered


@experiences_router.put('/{experience_id}', response_model=ExperienceResponse)
def update_experience(
    experience_update_info: ExperienceUpdateInfo,
    verified_user: int = Depends(oauth2.get_verified_user),
    db_session=Depends(database.get_db_session)
):
    experience = experiences.get_experience_by_id(
        db_session=db_session,
        experience_id=experience_update_info.experience_id
    )

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Experience not found'
        )

    if str(verified_user.user_id) != str(experience.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform requested action'
        )

    updated_experience = experiences.update_experience(
        db_session=db_session, experience_update_info=experience_update_info
    )

    updated_experience = utils.add_lifetime_to_experience(
        experience=updated_experience, created_at=updated_experience.created_at
    )

    return updated_experience


@experiences_router.delete(
    '/{experience_id}', response_model=ExperienceResponse
)
def delete_experience(
    experience_id: str,
    verified_user: int = Depends(oauth2.get_verified_user),
    db_session=Depends(database.get_db_session)
):
    experience = experiences.get_experience_by_id(
        db_session=db_session, experience_id=experience_id
    )

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Experience not found'
        )

    if str(verified_user.user_id) != str(experience.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform requested action'
        )

    deleted_experience = experiences.delete_experience(
        db_session=db_session, experience_id=experience_id
    )

    deleted_experience = utils.add_lifetime_to_experience(
        experience=deleted_experience, created_at=deleted_experience.created_at
    )

    return deleted_experience
