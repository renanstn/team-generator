import random

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import Event, Player
from database import engine


app = FastAPI()

# Prepare API to use Jinja2 templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Endpoints
@app.get("/ping")
async def ping():
    return {"message": "pong!"}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "eventos": [
                {
                    "title": "Volei",
                    "data": "2023-01-01",
                    "players": ["Renan", "Ju", "Mabel"],
                },
                {
                    "title": "Tabacaria",
                    "data": "2023-01-01",
                    "players": ["Iza", "Will"],
                },
            ],
        },
    )


@app.get("/events")
async def get_events():
    with Session(engine) as db_session:
        query = select(Event).where(Event.active == True)
        results = db_session.scalars(query)
        return results.all()


# @app.post("/events", response_model=Event)
# async def create_event(event: Event):
#     try:
#         with Session(engine) as db_session:
#             db_session.add(event)
#             db_session.commit()
#             db_session.refresh(event)
#             return event
#     except IntegrityError:
#         return {"message": "The event name must be unique."}


# @app.post("/event/{event_id}")
# async def join_event(event_id: int, player: Player):
#     with Session(database_engine) as db_session:
#         query = select(Event).where(Event.id == event_id)
#         results = db_session.exec(query)
#         event = results.one()
#         player.event_id = event.id
#         db_session.add(player)
#         db_session.commit()
#         db_session.refresh(player)
#     return player


# @app.get("/event/{event_id}/players")
# async def list_players(event_id: int):
#     with Session(database_engine) as db_session:
#         query = select(Player).where(Player.event_id == event_id)
#         results = db_session.exec(query)
#         players = results.all()
#     return players


# @app.post("/event/{event_id}/start")
# async def generate_teams(event_id: int):
#     with Session(database_engine) as db_session:
#         query_event = select(Event).where(Event.id == event_id)
#         event = db_session.exec(query_event).one()
#         max_players_on_team = event.max_member_for_team

#         query_players = select(Player).where(Player.event_id == event_id)
#         players = db_session.exec(query_players).all()

#     # Shuffle players
#     random.shuffle(players)

#     # Divide teams
#     teams = {}
#     teams_generated = 0

#     for i in range(0, len(players), max_players_on_team):
#         team = players[i : i + max_players_on_team]
#         teams.update({f"team {teams_generated}": team})
#         teams_generated += 1

#     return {"teams": teams}
