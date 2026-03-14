from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_create_application():
    payload = {
        "full_name": "Test User",
        "age": 40,
        "smoker": "no",
        "annual_income": 75000,
        "coverage_amount": 200000
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 200


def test_sample_decision():
    response = client.get("/sample-decision")
    assert response.status_code == 200

