import unittest

from fastapi.testclient import TestClient

from main import app, database_engine
from models import Event, Player


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Cria tabelas no banco de dados de teste
        Event.__table__.create(database_engine)
        Player.__table__.create(database_engine)

    def tearDown(self):
        # Exclui tabelas do banco de dados de teste
        Event.__table__.drop(database_engine)
        Player.__table__.drop(database_engine)

    def test_get_events(self):
        # Insere eventos de teste
        with database_engine.begin() as connection:
            connection.execute(Event.__table__.insert(), [
                {"name": "Event 1", "max_member_for_team": 5, "active": True},
                {"name": "Event 2", "max_member_for_team": 3, "active": True},
                {"name": "Event 3", "max_member_for_team": 2, "active": False},
            ])

        response = self.client.get("/events")
        self.assertEqual(response.status_code, 200)
        events = response.json()
        self.assertEqual(len(events), 2)

    def test_create_event(self):
        event_data = {
            "name": "New Event",
            "max_member_for_team": 4,
            "active": True,
        }
        response = self.client.post("/events", json=event_data)
        self.assertEqual(response.status_code, 200)
        event = response.json()
        self.assertEqual(event["name"], "New Event")

    def test_join_event(self):
        # Insere evento de teste
        with database_engine.begin() as connection:
            connection.execute(Event.__table__.insert(), {"name": "Event 1", "max_member_for_team": 5, "active": True})

        event_id = 1
        player_data = {"name": "Player 1"}

        response = self.client.post(f"/event/{event_id}", json=player_data)
        self.assertEqual(response.status_code, 200)
        player = response.json()
        self.assertEqual(player["name"], "Player 1")
        self.assertEqual(player["event_id"], event_id)

    def test_list_players(self):
        # Insere evento e jogadores de teste
        with database_engine.begin() as connection:
            connection.execute(Event.__table__.insert(), {"name": "Event 1", "max_member_for_team": 5, "active": True})
            connection.execute(Player.__table__.insert(), [
                {"name": "Player 1", "event_id": 1},
                {"name": "Player 2", "event_id": 1},
                {"name": "Player 3", "event_id": 2},
            ])

        event_id = 1
        response = self.client.get(f"/event/{event_id}/players")
        self.assertEqual(response.status_code, 200)
        players = response.json()
        self.assertEqual(len(players), 2)
