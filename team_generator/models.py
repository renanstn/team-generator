from typing import Optional

from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    max_member_for_team: int
    done: bool = False
