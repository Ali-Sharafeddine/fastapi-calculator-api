from fastapi.testclient import TestClient
from main import app
import sqlite3
from database import create_table, save_calculation, get_calculations

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add():
    response = client.get("/add?a=10&b=5")

    assert response.status_code == 200
    assert response.json()["result"] == 15

def test_subtract():
    response = client.get("/subtract?a=10&b=5")

    assert response.status_code == 200
    assert response.json()["result"] == 5

def test_divide():
    response = client.get("/divide?a=10&b=2")

    assert response.status_code == 200
    assert response.json()["result"] == 5.0


def test_divide_by_zero():
    response = client.get("/divide?a=10&b=0")

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot divide by zero."


def test_calculate_add():
    response = client.post(
        "/calculate",
        json={
            "a": 10,
            "b": 5,
            "operation": "add"
        }
    )

    assert response.status_code == 200
    assert response.json()["result"] == 15.0

def test_calculate_subtract():
    response = client.post(
        "/calculate",
        json={
            "a": 10,
            "b": 5,
            "operation": "subtract"
        }
    )

    assert response.status_code == 200
    assert response.json()["result"] == 5.0


def test_calculate_divide():
    response = client.post(
        "/calculate",
        json={
            "a": 10,
            "b": 2,
            "operation": "divide"
        }
    )

    assert response.status_code == 200
    assert response.json()["result"] == 5.0


def test_calculate_divide_by_zero():
    response = client.post(
        "/calculate",
        json={
            "a": 10,
            "b": 0,
            "operation": "divide"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot divide by zero."


def test_calculate_unsupported_operation():
    response = client.post(
        "/calculate",
        json={
            "a": 10,
            "b": 5,
            "operation": "power"
        }
    )

    assert response.status_code == 422


def test_calculate_invalid_type():
    response = client.post(
        "/calculate",
        json={
            "a": "hello",
            "b": 5,
            "operation": "add"
        }
    )

    assert response.status_code == 422


def test_calculate_missing_field():
    response = client.post(
        "/calculate",
        json={
            "a": 10,
            "operation": "add"
        }
    )

    assert response.status_code == 422


def test_delete_calculation(tmp_path, monkeypatch):
    test_db = tmp_path / "test_calculator.db"

    monkeypatch.setattr(
        "database.get_connection",
        lambda: sqlite3.connect(test_db)
    )

    create_table()

    save_calculation(10, 5, "add", 15)

    rows = get_calculations()
    calculation_id = rows[0][0]

    response = client.delete(f"/calculations/{calculation_id}")

    assert response.status_code == 200
    assert response.json()["deleted_id"] == calculation_id

    response = client.delete(f"/calculations/{calculation_id}")

    assert response.status_code == 404