from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Hello(Base):
    __tablename__ = "hello"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date = Column(Date)
    image = Column(String, nullable=True)
    closed = Column(Boolean, default=False)
    players = relationship("Player", back_populates="game")


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    game_id = Column(Integer, ForeignKey("game.id"))
    game = relationship("Game", back_populates="players")
