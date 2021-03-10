from fastapi.testclient import TestClient
from ...controllers.main import app

# create a client for testing
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    
