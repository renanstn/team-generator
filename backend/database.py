from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = config(
    "DATABASE_URL", default="postgresql://postgres:postgres@db:5432/postgres"
)
DATABASE_DEBUG = config("DATABASE_DEBUG", cast=bool, default=False)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Serve a database session and close it at the end.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
