# libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# local libraries
from app.app import app
from app import database
from app.config import settings


SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{settings.db_user}:{settings.db_password}'
    f'@{settings.db_host}:{settings.db_port}/{settings.db_name}_test'
)

# create engine to interact with DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create class to create session
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# used to define DB architecture
Base = declarative_base()

# create DB
Base.metadata.create_all(bind=engine)

# create a session with SessionLocal
def override_get_db_session() -> Session:
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


app.dependency_overrides[database.get_db_session] = override_get_db_session
