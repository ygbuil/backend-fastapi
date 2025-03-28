"""Authentication module."""

import datetime
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from backend_fastapi import data
from backend_fastapi.data import settings
from backend_fastapi.endpoint_functions import users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(username: str, user_id: UUID, color: str, expiration_time: int) -> str:
    """Create token for the user."""
    expire_date = datetime.datetime.now(tz=datetime.UTC) + expiration_time
    return jwt.encode(
        {
            "username": username,
            "user_id": str(user_id),
            "color": str(color),
            "exp": expire_date,
        },
        key=settings.secret_key,
        algorithm="HS256",
    )


def get_verified_user(
    token: str = Depends(oauth2_scheme),
    db_session: Depends = Depends(data.get_db_session),  # noqa: B008
) -> dict:
    """Get the authorised user for the received token."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms="HS256")
        return users.get_user_by_id(db_session=db_session, user_id=payload.get("user_id"))

    except JWTError as exc:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
        ) from exc
