import string
import random
from typing import Union, List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
import models, schemas


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/ping")
async def ping():
    """
    Endpoint for connection test purposes.
    """
    return {"message": "pong!"}


@app.get("/test_db", response_model=Union[schemas.HelloSchema, dict])
async def test_database_connection(db: Session = Depends(get_db)):
    """
    Endpoint for database connection test purposes.
    """
    data = db.query(models.Hello).first()
    return data if data else {"message": "The database is empty."}


@app.get("/games", response_model=List[schemas.GameSchema])
async def list_games(db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um jogo do banco de dados.
    """
    data = db.query(models.Game).all()
    return data


@app.post("/game", response_model=schemas.GameSchema)
async def create_game(
    game: schemas.GameInSchema, db: Session = Depends(get_db)
):
    """
    Endpoint for game creation.
    """
    game_to_create = models.Game(**game.model_dump())
    db.add(game_to_create)
    db.commit()
    db.refresh(game_to_create)
    return game_to_create


@app.get("/players", response_model=List[schemas.PlayerSchema])
async def list_players(db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um jogador do banco de dados.
    """
    data = db.query(models.Player).all()
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


# @app.post("/generate_teams", response_model=List[schemas.TeamsSchema])
@app.post("/generate_teams")
async def generate_teams(game_id: int, db: Session = Depends(get_db)):
    """
    Generate game teams with random players
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
    teams_to_be_saved = []
    teams = [
        players[i : i + game.max_players_per_teams]
        for i in range(0, len(players), game.max_players_per_teams)
    ]
    letters = string.ascii_uppercase
    for team in teams:
        for index, player in enumerate(team):
            teams_to_be_saved.append(
                schemas.PlayerTeamInSchema(
                    name=f"Team {letters[index]}",
                    player_id=player.id,
                    game_id=game.id,
                )
            )
    db.bulk_insert_mappings(
        models.PlayerTeam, [i.dict() for i in teams_to_be_saved]
    )
    db.commit()
