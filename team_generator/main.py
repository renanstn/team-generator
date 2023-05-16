from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel, Session, select
from decouple import config
from sqlalchemy.exc import IntegrityError

from models import Event, Player


DATABASE_URL = config(
    "DATABASE_URL", default="postgresql://postgres:postgres@db:5432/postgres"
)
DATABASE_DEBUG = config("DATABASE_DEBUG", cast=bool, default=False)

app = FastAPI()

database_engine = create_engine(DATABASE_URL, echo=DATABASE_DEBUG)
SQLModel.metadata.create_all(database_engine)


@app.get("/hello")
async def hello():
    return {"hello": "world"}

@app.get("/events")
async def get_events():

    with Session(database_engine) as db_session:
        query = select(Event).where(Event.active == True)
        results = db_session.exec(query)
        return results.all()

@app.post("/events")
async def create_event(event: Event):
    try:
        with Session(database_engine) as db_session:
            db_session.add(event)
            db_session.commit()
            db_session.refresh(event)
    except IntegrityError:
        return {"message": "The event name must be unique."}
    return event

@app.post("/event/{event_id}")
async def join_event(event_id: int, player: Player):
    with Session(database_engine) as db_session:
        query = select(Event).where(Event.id == event_id)
        results = db_session.exec(query)
        event = results.one()
        player.event_id = event.id
        db_session.add(player)
        db_session.commit()
        db_session.refresh(player)
    return player

@app.get("/event/{event_id}/players")
async def list_players(event_id: int):
    with Session(database_engine) as db_session:
        query = select(Player).where(Player.event_id == event_id)
        results = db_session.exec(query)
        players = results.all()
    return players
