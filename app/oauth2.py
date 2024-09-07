# libraries
from datetime import datetime
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config import settings
from app.database import get_db_session

# local libraries
from app.functions.crud import users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(username: str, user_id: UUID, color: str, expiration_time):
    expire_date = datetime.utcnow() + expiration_time
    encoded_token = jwt.encode(
        {
            "username": username,
            "user_id": str(user_id),
            "color": str(color),
            "exp": expire_date,
        },
        key=settings.secret_key,
        algorithm="HS256",
    )

    return encoded_token


def get_verified_user(token: str = Depends(oauth2_scheme), db_session=Depends(get_db_session)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms="HS256")
        verified_user = users.get_user_by_id(db_session=db_session, user_id=payload.get("user_id"))

        return verified_user

    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Could not validate token")
