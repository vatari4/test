from src.models.hero import Hero
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class HeroUseCase:
    def __init__(self):
        self.superhero_api_token = os.getenv("SUPERHERO_API_TOKEN")
        self.superhero_api_url = "https://superheroapi.com/api"

    def search_hero(self, name: str) -> dict:
        url = f"{self.superhero_api_url}/{self.superhero_api_token}/search/{name}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("response") == "success" and data.get("results"):
                return data["results"][0]  # Return first matching hero
        return None

    def safe_int(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def add_hero_to_db(self, hero_data: dict, db):
        existing_hero = db.query(Hero).filter(Hero.name == hero_data["name"]).first()
        if existing_hero:
            return existing_hero

        powerstats = hero_data.get("powerstats", {})

        new_hero = Hero(
            name=hero_data["name"],
            intelligence=self.safe_int(powerstats.get("intelligence")),
            strength=self.safe_int(powerstats.get("strength")),
            speed=self.safe_int(powerstats.get("speed")),
            power=self.safe_int(powerstats.get("power")),
        )

        db.add(new_hero)
        db.commit()
        db.refresh(new_hero)
        return new_hero

    def get_heroes(self, db, name=None, intelligence=None, strength=None, speed=None, power=None):
        query = db.query(Hero)

        if name:
            query = query.filter(Hero.name == name)
        if intelligence is not None:
            query = query.filter(Hero.intelligence == intelligence)
        if strength is not None:
            query = query.filter(Hero.strength == strength)
        if speed is not None:
            query = query.filter(Hero.speed == speed)
        if power is not None:
            query = query.filter(Hero.power == power)

        return query.all()
