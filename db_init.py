# local libraries
from app.models import Base
from app.database import engine


# create DB
Base.metadata.create_all(bind=engine)
