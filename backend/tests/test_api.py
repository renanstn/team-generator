import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_db
from database import Base


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        # Setup sqlite database for tests
        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = self.override_get_db
        # Create the test client
        self.client = TestClient(app)

    def override_get_db(self):
        try:
            db = self.TestingSessionLocal()
            yield db
        finally:
            db.close()

    def test_hello(self):
        """
        The hello endpoint must return a simple message.
        """
        response = self.client.get("/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "pong!"})

    def test_database_connection_without_data(self):
        """
        The test_db endpoint must connect to the database to get some data and
        return the value loaded.
        """
        response = self.client.get("/test_db")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"message": "The database is empty."}
        )

    def test_create_game(self):
        """
        It must be possible create games on /game endpoint.
        """
        payload = {
            "name": "test",
            "date": "2020-01-01",
            "max_players_per_teams": 4,
            "image": "",
        }
        # Create game
        response = self.client.post("/game", json=payload)
        self.assertEqual(response.status_code, 200)
        # Get game id returned from endpoint
        game_id = response.json()["id"]
        # Check if the game was really created on the database
        created_game = self.client.get(f"/game/{game_id}")
        self.assertEqual(created_game.status_code, 200)
        self.assertEqual(created_game.json()["name"], payload["name"])
        self.assertEqual(
            created_game.json()["max_players_per_teams"],
            payload["max_players_per_teams"],
        )
        self.assertEqual(created_game.json()["date"], payload["date"])

    def test_create_player(self):
        """
        It must be possible to join players on /player endpoint.
        """
        # First, create the game
        game_payload = {
            "name": "test",
            "date": "2020-01-01",
            "max_players_per_teams": 4,
            "image": "",
        }
        response = self.client.post("/game", json=game_payload)
        self.assertEqual(response.status_code, 200)
        # Get game id returned from endpoint
        game_id = response.json()["id"]
        # Now, add players to the game
        players_payload = [
            {"name": "player A"},
            {"name": "player B"},
            {"name": "player C"},
        ]
        for player in players_payload:
            response = self.client.post(
                f"/player?game_id={game_id}", json=player
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["name"], player["name"])
            self.assertEqual(response.json()["game_id"], game_id)
