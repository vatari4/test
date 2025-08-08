from fastapi import APIRouter, Depends
from src.controller.hero_controller import create_hero, get_heroes
from src.models.schemas import HeroCreate, HeroRead
from sqlalchemy.orm import Session
from src.models.db import get_db
from typing import Optional

router = APIRouter()

@router.post("/hero/", response_model=HeroRead)
async def create_hero_endpoint(
    hero_data: HeroCreate,
    db: Session = Depends(get_db)
):
    return create_hero(hero_data, db)

@router.get("/hero/", response_model=list[HeroRead])
async def get_heroes_endpoint(
    name: Optional[str] = None,
    intelligence: Optional[int] = None,
    strength: Optional[int] = None,
    speed: Optional[int] = None,
    power: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return get_heroes(
        name=name,
        intelligence=intelligence,
        strength=strength,
        speed=speed,
        power=power,
        db=db
    )
