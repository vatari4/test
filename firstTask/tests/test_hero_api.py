import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app

client = TestClient(app)

@pytest.fixture
def hero_data():
    return {
        "name": "Batman",
        "powerstats": {
            "intelligence": "90",
            "strength": "25",
            "speed": "30",
            "power": "40"
        }
    }

def test_create_hero_success(hero_data):
    with patch("src.controller.hero_controller.hero_usecase") as mock_usecase:
        mock_usecase.search_hero.return_value = hero_data
        mock_usecase.add_hero_to_db.return_value = {
            "id": 1,
            "name": hero_data["name"],
            "intelligence": 90,
            "strength": 25,
            "speed": 30,
            "power": 40
        }

        response = client.post("/hero/", json={"name": "Batman"})
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["name"] == "Batman"
        assert json_data["intelligence"] == 90

def test_create_hero_not_found():
    with patch("src.controller.hero_controller.hero_usecase") as mock_usecase:
        mock_usecase.search_hero.return_value = None

        response = client.post("/hero/", json={"name": "UnknownHero"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Hero not found"

def test_get_heroes_success():
    with patch("src.controller.hero_controller.hero_usecase") as mock_usecase:
        mock_usecase.get_heroes.return_value = [
            {
                "id": 1,
                "name": "Batman",
                "intelligence": 90,
                "strength": 25,
                "speed": 30,
                "power": 40
            }
        ]

        response = client.get("/hero/?name=Batman")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["name"] == "Batman"

def test_get_heroes_not_found():
    with patch("src.controller.hero_controller.hero_usecase") as mock_usecase:
        mock_usecase.get_heroes.return_value = []

        response = client.get("/hero/?name=Unknown")
        assert response.status_code == 404
        assert response.json()["detail"] == "No heroes found with these parameters"
