from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add():
    response = client.get("/add?a=10&b=5")

    assert response.status_code == 200
    assert response.json()["result"] == 15


def test_divide():
    response = client.get("/divide?a=10&b=2")

    assert response.status_code == 200
    assert response.json()["result"] == 5.0

def test_divide_by_zero():
    response = client.get("/divide?a=10&b=0")

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot divide by zero."