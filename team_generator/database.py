from decouple import config
from sqlalchemy import create_engine

from models import Base

DATABASE_URL = config(
    "DATABASE_URL", default="postgresql://postgres:postgres@db:5432/postgres"
)
DATABASE_DEBUG = config("DATABASE_DEBUG", cast=bool, default=False)


engine = create_engine(DATABASE_URL, echo=DATABASE_DEBUG)

# Init all tables
Base.metadata.create_all(engine)
