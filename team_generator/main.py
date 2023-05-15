from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel, Session, select
from decouple import config

from models import Event


DATABASE_URL = config(
    "DATABASE_URL", default="postgresql://postgres:postgres@db:5432/postgres"
)
DATABASE_DEBUG = config("DATABASE_DEBUG", cast=bool, default=False)

app = FastAPI()

database_engine = create_engine(DATABASE_URL, echo=DATABASE_DEBUG)
SQLModel.metadata.create_all(database_engine)


@app.get("/hello")
async def hello():
    test = Event(name="event test", max_member_for_team=4)

    with Session(database_engine) as db_session:
        db_session.add(test)
        db_session.commit()

    with Session(database_engine) as db_session:
        statement = select(Event)
        results = db_session.exec(statement)
        for i in results:
            print(i)

    return {"hello": "world"}
