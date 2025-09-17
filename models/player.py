from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    first_login_at = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    daily_score = Column(Integer, default=0)

    boosts = relationship("PlayerBoost", back_populates="player")


class Boost(Base):
    __tablename__ = "boosts"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)


class PlayerBoost(Base):
    __tablename__ = "player_boosts"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    boost_id = Column(Integer, ForeignKey("boosts.id"))
    acquired_at = Column(DateTime, default=func.now())
    manual = Column(Boolean, default=False)

    player = relationship("Player", back_populates="boosts")
    boost = relationship("Boost")
