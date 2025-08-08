from pydantic import BaseModel

class HeroCreate(BaseModel):
    name: str

class HeroRead(BaseModel):
    id: int
    name: str
    intelligence: int
    strength: int
    speed: int
    power: int

    class Config:
        orm_mode = True