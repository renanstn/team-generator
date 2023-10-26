from datetime import date

from pydantic import BaseModel


class HelloSchema(BaseModel):
    id: int
    name: str


class GameSchema(BaseModel):
    pass


class GameInSchema(BaseModel):
    name: str
    date: date
    image: str = None
