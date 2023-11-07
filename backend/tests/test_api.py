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
            "max_players_per_team": 4,
            "image": "",
        }

        # Create game
        response = self.client.post("/game", json=payload)
        self.assertEqual(response.status_code, 200)
        # Get game id returned from endpoint
        game_id = response.json()["id"]

        # Check if game return in a list of games
        response = self.client.get("/games")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        # Check if the game was really created on the database
        created_game = self.client.get(f"/game/{game_id}")
        self.assertEqual(created_game.status_code, 200)
        self.assertEqual(created_game.json()["name"], payload["name"])
        self.assertEqual(
            created_game.json()["max_players_per_team"],
            payload["max_players_per_team"],
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
            "max_players_per_team": 4,
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

        # Get these players and check
        players = self.client.get("/players")
        self.assertEqual(players.status_code, 200)
        self.assertEqual(len(players.json()), 3)
        for index, expected_player in enumerate(players_payload):
            self.assertEqual(
                players.json()[index]["name"], expected_player["name"]
            )
            self.assertEqual(players.json()[index]["game_id"], 1)

    def test_generate_teams(self):
        """
        Given a game and a few players, it must be possible to generate teams
        for this game.
        """
        # Create game
        game_payload = {
            "name": "test",
            "date": "2020-01-01",
            "max_players_per_team": 2,
            "image": "",
        }
        response = self.client.post("/game", json=game_payload)
        self.assertEqual(response.status_code, 200)
        game_id = response.json()["id"]

        # Add players
        players_payload = [
            {"name": "player A"},
            {"name": "player B"},
            {"name": "player C"},
            {"name": "player D"},
            {"name": "player E"},
        ]
        for player in players_payload:
            response = self.client.post(
                f"/player?game_id={game_id}", json=player
            )
            self.assertEqual(response.status_code, 200)

        # Generate teams
        response = self.client.post(f"/generate_teams?game_id={game_id}")
        self.assertEqual(response.status_code, 200)
        generated_teams = self.client.get(f"/teams/{game_id}")
        self.assertEqual(generated_teams.status_code, 200)

        # 3 teams must be created, 2 teams with 2 players each, and one team
        # with only one player.
        self.assertEqual(len(generated_teams.json()), 3)
        self.assertEqual(len(generated_teams.json()[0]["players"]), 2)
        self.assertEqual(len(generated_teams.json()[1]["players"]), 2)
        self.assertEqual(len(generated_teams.json()[2]["players"]), 1)
