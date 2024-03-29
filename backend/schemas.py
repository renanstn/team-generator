from typing import List
from datetime import date

from pydantic import BaseModel


class HelloSchema(BaseModel):
    id: int
    name: str


class PlayerSchema(BaseModel):
    id: int
    name: str
    game_id: int


class PlayerInSchema(BaseModel):
    name: str


class GameSchema(BaseModel):
    id: int
    name: str
    date: date
    max_players_per_team: int
    players: List[PlayerSchema]


class GameInSchema(BaseModel):
    name: str
    date: date
    max_players_per_team: int
    image: str = None


class TeamSchema(BaseModel):
    name: str
    players: List[PlayerSchema]


class TeamInSchema(BaseModel):
    name: str
    game_id: int
