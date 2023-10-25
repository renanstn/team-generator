import unittest

from fastapi.testclient import TestClient

from main import app


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_hello(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})

    def test_database_connection(self):
        response = self.client.get("/test_db")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Stored value": "test"})
