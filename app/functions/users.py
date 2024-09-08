"""Functions that deal with users."""

from sqlalchemy.orm import Session

from app.functions import utils
from app.models import UsersTableItem
from app.schemas import NewUser, UserUpdateInfo


def create_user(db_session: Session, user_to_create: NewUser) -> UsersTableItem:
    """Create a user and write it to database."""
    user_to_create.password = utils.hash_password(user_to_create.password)
    new_user = UsersTableItem(**user_to_create.dict())

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return new_user


def get_user_by_name(db_session: Session, username: str) -> UsersTableItem:
    """Get user by name from database."""
    return db_session.query(UsersTableItem).filter(UsersTableItem.username == username).first()


def get_user_by_id(db_session: Session, user_id: str) -> UsersTableItem:
    """Get user by id from database."""
    return db_session.query(UsersTableItem).filter(UsersTableItem.user_id == user_id).first()


def update_user(db_session: Session, user_update_info: UserUpdateInfo) -> UsersTableItem:
    """Update user info and write it to database."""
    user = get_user_by_id(db_session, user_update_info.user_id)

    for key, value in user_update_info.dict().items():
        if value is not None:
            setattr(user, key, value)

    db_session.commit()
    db_session.refresh(user)

    return user


def delete_user(db_session: Session, user_id: str) -> UsersTableItem:
    """Create user from database."""
    user = get_user_by_id(db_session=db_session, user_id=user_id)

    db_session.delete(user)
    db_session.commit()

    return user
