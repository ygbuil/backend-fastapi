# libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# local libraries
from app.config import settings


SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{settings.db_user}:{settings.db_password}'
    f'@{settings.db_host}:{settings.db_port}/{settings.db_name}'
)

# create engine to interact with DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create class to create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# used to define DB architecture
Base = declarative_base()

# create a session with SessionLocal
def get_db_session() -> Session:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
