"""Functions that deal with users."""

from passlib.context import CryptContext  # type: ignore
from sqlalchemy.orm import Session

from backend_fastapi.data import NewUser, UsersTableItem, UserUpdateInfo

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db_session: Session, user_to_create: NewUser) -> UsersTableItem:
    """Create a user and write it to database."""
    user_to_create.password = _hash_password(user_to_create.password)
    new_user = UsersTableItem(**user_to_create.model_dump())

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return new_user


def get_user_by_name(db_session: Session, username: str) -> UsersTableItem | None:
    """Get user by name from database."""
    return db_session.query(UsersTableItem).filter(UsersTableItem.username == username).first()


def get_user_by_id(db_session: Session, user_id: str) -> UsersTableItem | None:
    """Get user by id from database."""
    return db_session.query(UsersTableItem).filter(UsersTableItem.user_id == user_id).first()


def update_user(
    db_session: Session, user: UsersTableItem, user_update_info: UserUpdateInfo
) -> UsersTableItem:
    """Update user info and write it to database."""
    for key, value in user_update_info.model_dump().items():
        if value is not None:
            setattr(user, key, value)

    db_session.commit()
    db_session.refresh(user)

    return user


def delete_user(db_session: Session, user: str) -> UsersTableItem:
    """Create user from database."""
    db_session.delete(user)
    db_session.commit()

    return user


def _hash_password(password: str) -> str:
    """Hash password."""
    return PWD_CONTEXT.hash(password)  # type: ignore
