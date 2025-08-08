from sqlalchemy import Column, Integer, String
from .db import Base

class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    intelligence = Column(Integer)
    strength = Column(Integer)
    speed = Column(Integer)
    power = Column(Integer)

    def __repr__(self):
        return f"<Hero(name='{self.name}', intelligence={self.intelligence}, strength={self.strength}, speed={self.speed}, power={self.power})>"
