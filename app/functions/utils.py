# libraries
import datetime
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def add_lifetime_to_experience(experience, created_at: datetime):
    time_dif = datetime.datetime.today() - created_at.replace(tzinfo=None)
    time_dif = time_dif.days

    year = int(time_dif/365)
    week = int((time_dif%365)/7)
    days = int((time_dif%365)%7)

    lifetime = ''

    if year != 0:
        lifetime = lifetime + str(year) + 'y, '
    if week != 0:
        lifetime = lifetime + str(week) + 'w, '
    if days != 0:
        lifetime = lifetime + str(days) + 'd, '

    if lifetime == '':
        lifetime = 'today'
    else:
        lifetime = lifetime[:-2] + ' ago'

    experience.lifetime = lifetime

    return experience
