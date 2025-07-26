"""Config package variables."""

from passlib.context import CryptContext  # type: ignore

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
