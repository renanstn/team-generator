from datetime import date

from pydantic import BaseModel


class HelloSchema(BaseModel):
    id: int
    name: str


class GameSchema(BaseModel):
    id: int
    name: str
    date: date


class GameInSchema(BaseModel):
    name: str
    date: date
    image: str = None


class PlayerSchema(BaseModel):
    id: int
    name: str
    game_id: int


class PlayerInSchema(BaseModel):
    name: str
