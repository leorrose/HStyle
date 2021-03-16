"""
Tests for main controller
"""

from requests import Response
from fastapi.testclient import TestClient
from server.controllers.main import app


# create a client for testing
client: TestClient = TestClient(app)


def test_main_api_end_point() -> None:
    """
    Test method of main controller api end point
    """
    # Act
    response: Response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert response.url == 'http://testserver/docs'
