# libraries
from fastapi import APIRouter, Depends, HTTPException, status

# local libraries
from app import database, oauth2
from app.functions.crud import users
from app.schemas import NewUser, UserResponse, UserUpdateInfo

users_router = APIRouter(prefix="/users")


@users_router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_to_create: NewUser, db_session=Depends(database.get_db_session)):
    user = users.get_user_by_name(db_session=db_session, username=user_to_create.username)

    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    created_user = users.create_user(db_session=db_session, user_to_create=user_to_create)

    return created_user


@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db_session=Depends(database.get_db_session)):
    user = users.get_user_by_id(db_session=db_session, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@users_router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    user_update_info: UserUpdateInfo,
    verified_user=Depends(oauth2.get_verified_user),
    db_session=Depends(database.get_db_session),
):
    try:
        user_to_update = users.get_user_by_id(db_session=db_session, user_id=user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    if user_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if str(verified_user.user_id) != str(user_to_update.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    updated_user = users.update_user(db_session=db_session, user_update_info=user_update_info)

    return updated_user


@users_router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: str,
    verified_user=Depends(oauth2.get_verified_user),
    db_session=Depends(database.get_db_session),
):
    user_to_delete = users.get_user_by_id(db_session=db_session, user_id=user_id)

    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if str(verified_user.user_id) != str(user_to_delete.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    deleted_user = users.delete_user(db_session=db_session, user_id=user_to_delete.user_id)

    return deleted_user
