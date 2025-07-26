"""Users endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend_fastapi import data, endpoint_functions
from backend_fastapi.data import NewUser, UserResponse, UsersTableItem, UserUpdateInfo

users_router = APIRouter(prefix="/users")


@users_router.post("", status_code=status.HTTP_201_CREATED)
def create_user(
    user_to_create: NewUser,
    db_session: Annotated[Session, Depends(data.get_db_session)],
) -> UserResponse:
    """Create user endpoint."""
    user = endpoint_functions.get_user_by_name(
        db_session=db_session,
        username=user_to_create.username,
    )

    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    return endpoint_functions.create_user(db_session=db_session, user_to_create=user_to_create)


@users_router.get("/{user_id}")
def get_user(
    user_id: str, db_session: Annotated[Session, Depends(data.get_db_session)]
) -> UserResponse:
    """Get user endpoint."""
    user = endpoint_functions.get_user_by_id(db_session=db_session, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@users_router.put("/{user_id}")
def update_user(
    user_id: str,
    user_update_info: UserUpdateInfo,
    verified_user: Annotated[UsersTableItem, Depends(endpoint_functions.get_verified_user)],
    db_session: Annotated[Session, Depends(data.get_db_session)],
) -> UserResponse:
    """Update user endpoint."""
    try:
        user = endpoint_functions.get_user_by_id(db_session=db_session, user_id=user_id)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request") from exc

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if str(verified_user.user_id) != str(user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    return endpoint_functions.update_user(
        db_session=db_session, user=user, user_update_info=user_update_info
    )


@users_router.delete("/{user_id}")
def delete_user(
    user_id: str,
    verified_user: Annotated[UsersTableItem, Depends(endpoint_functions.get_verified_user)],
    db_session: Annotated[Session, Depends(data.get_db_session)],
) -> UserResponse:
    """Delete user endpoint."""
    user = endpoint_functions.get_user_by_id(db_session=db_session, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if str(verified_user.user_id) != str(user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    return endpoint_functions.delete_user(db_session=db_session, user=user)
