import string
import random
from typing import Union, List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
import models, schemas


# Create models if not exist
models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Tests endpoints -------------------------------------------------------------
@app.get("/ping")
async def ping():
    return {"message": "pong!"}


@app.get("/test_db", response_model=Union[schemas.HelloSchema, dict])
async def test_database_connection(db: Session = Depends(get_db)):
    data = db.query(models.Hello).first()
    return data if data else {"message": "The database is empty."}


# Games endpoints -------------------------------------------------------------
@app.get("/games", response_model=List[schemas.GameSchema])
async def list_games(db: Session = Depends(get_db)):
    data = db.query(models.Game).all()
    return data


@app.get("/game/{game_id}", response_model=schemas.GameSchema)
async def get_game(game_id: int, db: Session = Depends(get_db)):
    data = db.query(models.Game).filter(models.Game.id == game_id).first()
    return data


@app.post("/game", response_model=schemas.GameSchema)
async def create_game(
    game: schemas.GameInSchema, db: Session = Depends(get_db)
):
    game_to_create = models.Game(**game.model_dump())
    db.add(game_to_create)
    db.commit()
    db.refresh(game_to_create)
    return game_to_create


# Players endpoints -----------------------------------------------------------
@app.get("/players", response_model=List[schemas.PlayerSchema])
async def list_players(db: Session = Depends(get_db)):
    data = db.query(models.Player).all()
    return data


@app.get("/player/{player_id}", response_model=schemas.PlayerSchema)
async def get_game(player_id: int, db: Session = Depends(get_db)):
    data = (
        db.query(models.Player).filter(models.Player.id == player_id).first()
    )
    return data


@app.post("/player", response_model=Union[schemas.PlayerSchema, dict])
async def create_player(
    game_id: int, player: schemas.PlayerInSchema, db: Session = Depends(get_db)
):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        return {"message": f"Game id {game_id} not found."}
    player_to_create = models.Player(game_id=game_id, **player.model_dump())
    db.add(player_to_create)
    db.commit()
    db.refresh(player_to_create)
    return player_to_create


# Teams endpoints -------------------------------------------------------------
@app.get("/teams/{game_id}", response_model=List[schemas.TeamSchema])
async def get_game_teams(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        return {"message": f"Game id {game_id} not found."}
    data = db.query(models.Team).filter(models.Team.game_id == game_id).all()
    return data


# Actions endpoints -----------------------------------------------------------
@app.post("/generate_teams")
async def generate_teams(game_id: int, db: Session = Depends(get_db)):
    """
    Generate game teams with random players.
    """
    # Check if game exists
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        return {"message": f"Game id {game_id} not found."}

    # Check if game has players joined
    players = (
        db.query(models.Player).filter(models.Player.game_id == game_id).all()
    )
    if not players:
        return {"message": f"This game has no players subscribed."}

    # Shuffle players and create teams
    random.shuffle(players)
    teams = [
        players[i : i + game.max_players_per_teams]
        for i in range(0, len(players), game.max_players_per_teams)
    ]

    # Create teams on database and update players team id
    letters = string.ascii_uppercase
    for index, team in enumerate(teams):
        team_to_create = models.Team(
            name=f"Team {letters[index]}",
            game_id=game.id,
        )
        db.add(team_to_create)
        db.commit()
        db.refresh(team_to_create)
        for player in team:
            player.team_id = team_to_create.id
            db.commit()

    return {"message": "Teams generated!"}
