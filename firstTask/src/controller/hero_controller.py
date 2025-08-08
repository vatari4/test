from fastapi import HTTPException, Depends
from src.usecase.hero_usecase import HeroUseCase
from src.models.schemas import HeroCreate, HeroRead
from src.models.db import get_db
from sqlalchemy.orm import Session

hero_usecase = HeroUseCase()

def create_hero(hero_data: HeroCreate, db: Session = Depends(get_db)):
    hero = hero_usecase.search_hero(hero_data.name)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    db_hero = hero_usecase.add_hero_to_db(hero, db)
    return db_hero

def get_heroes(
        name: str = None,
        intelligence: int = None,
        strength: int = None,
        speed: int = None,
        power: int = None,
        db: Session = Depends(get_db)
):
    heroes = hero_usecase.get_heroes(
        db,
        name=name,
        intelligence=intelligence,
        strength=strength,
        speed=speed,
        power=power
    )

    if not heroes:
        raise HTTPException(status_code=404, detail="No heroes found with these parameters")

    return heroes
