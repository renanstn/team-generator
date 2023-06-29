from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(unique=True)
    max_member_for_team: int
    date: datetime
    active: bool = True


class Player(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(unique=True)
    event_id: Optional[int] = Field(foreign_key="event.id")
