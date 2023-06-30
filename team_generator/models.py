from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    max_member_for_team: Mapped[int]
    date: Mapped[datetime]
    active: Mapped[bool] = True
    players: Mapped["Player"] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return self.name


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))

    event: Mapped["Event"] = relationship(back_populates="players")

    def __repr__(self) -> str:
        return self.name
