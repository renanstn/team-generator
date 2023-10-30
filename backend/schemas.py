from typing import List
from datetime import date

from pydantic import BaseModel


class HelloSchema(BaseModel):
    id: int
    name: str


class GameSchema(BaseModel):
    id: int
    name: str
    date: date
    max_players_per_teams: int


class GameInSchema(BaseModel):
    name: str
    date: date
    max_players_per_teams: int
    image: str = None


class PlayerSchema(BaseModel):
    id: int
    name: str
    game_id: int


class PlayerInSchema(BaseModel):
    name: str


class TeamsSchema(BaseModel):
    id: int
    name: str
    game: GameSchema
    players: List[PlayerSchema]
