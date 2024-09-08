"""Utils functions."""

import datetime

from passlib.context import CryptContext

from app.models import ExperiencesTableItem

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password."""
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain text password matches hashed password."""
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def add_lifetime_to_experience(experience: ExperiencesTableItem, created_at: datetime) -> str:
    """Calculate the time that happened since a experience was created."""
    days_dif = (datetime.datetime.now(tz=datetime.timezone.utc) - created_at).days

    years = days_dif // 365
    weeks = int((days_dif % 365) / 7)
    days = int((days_dif % 365) % 7)

    lifetime = ""

    if years != 0:
        lifetime += str(years) + "y, "
    if weeks != 0:
        lifetime += str(weeks) + "w, "
    if days != 0:
        lifetime += str(days) + "d, "

    lifetime = "today" if lifetime == "" else lifetime[:-2] + " ago"
    experience.lifetime = lifetime

    return experience
