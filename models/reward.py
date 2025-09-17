from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .player import Base


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    order = Column(Integer, default=0)


class Prize(Base):
    __tablename__ = "prizes"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)


class PlayerLevel(Base):
    __tablename__ = "player_levels"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    level_id = Column(Integer, ForeignKey("levels.id"))
    completed = Column(Date, nullable=True)
    is_completed = Column(Boolean, default=False)
    score = Column(Integer, default=0)

    player = relationship("Player")
    level = relationship("Level")


class LevelPrize(Base):
    __tablename__ = "level_prizes"

    id = Column(Integer, primary_key=True)
    level_id = Column(Integer, ForeignKey("levels.id"))
    prize_id = Column(Integer, ForeignKey("prizes.id"))
    received = Column(Date, default=datetime.utcnow)

    level = relationship("Level")
    prize = relationship("Prize")
