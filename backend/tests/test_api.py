import unittest

from fastapi.testclient import TestClient

from main import app


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_hello(self):
        """
        The hello endpoint must return a simple message.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})

    def test_database_connection(self):
        """
        The test_db endpoint must connect to the database to get some data and
        return the value loaded.
        """
        response = self.client.get("/test_db")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Stored value": "test"})
