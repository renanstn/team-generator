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
    max_players_per_team = Column(Integer)
    image = Column(String, nullable=True)
    closed = Column(Boolean, default=False)
    players = relationship("Player", back_populates="game")
    teams = relationship("Team", back_populates="game")


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    game_id = Column(Integer, ForeignKey("game.id"))
    team_id = Column(Integer, ForeignKey("team.id"))
    game = relationship("Game", back_populates="players")
    team = relationship("Team", back_populates="players")


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    game_id = Column(Integer, ForeignKey("game.id"))
    game = relationship("Game", back_populates="teams")
    players = relationship("Player", back_populates="team")
