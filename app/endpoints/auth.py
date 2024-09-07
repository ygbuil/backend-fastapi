# libraries
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import database, oauth2
from app.functions import utils

# local libraries
from app.functions.crud import users

auth_router = APIRouter()


@auth_router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session=Depends(database.get_db_session),
):
    user = users.get_user_by_name(db_session=db_session, username=form_data.username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not utils.verify_password(plain_password=form_data.password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    access_token = oauth2.create_token(
        username=user.username,
        user_id=user.user_id,
        color=user.color,
        expiration_time=timedelta(minutes=30),
    )

    return {"access_token": access_token, "token_type": "bearer"}
