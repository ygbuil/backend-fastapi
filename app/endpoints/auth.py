"""Auth endpoints."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app import database
from app.endpoint_functions import auth, users

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


auth_router = APIRouter()


@auth_router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
    db_session: Depends = Depends(database.get_db_session),  # noqa: B008
) -> dict:
    """Get authentication bearer token."""
    user = users.get_user_by_name(db_session=db_session, username=form_data.username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not _verify_password(plain_password=form_data.password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    access_token = auth.create_token(
        username=user.username,
        user_id=user.user_id,
        color=user.color,
        expiration_time=timedelta(minutes=30),
    )

    return {"access_token": access_token, "token_type": "bearer"}


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain text password matches hashed password."""
    return PWD_CONTEXT.verify(plain_password, hashed_password)
