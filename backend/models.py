from sqlalchemy import Column, Integer, String

from database import Base


class Hello(Base):
    __tablename__ = "hello"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
