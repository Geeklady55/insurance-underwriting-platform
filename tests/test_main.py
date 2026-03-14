
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Insurance Underwriting API is running"}


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
    data = response.json()
    assert data["full_name"] == "Test User"
    assert "decision" in data


def test_sample_decision():
    response = client.get("/sample-decision")
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "decision" in data
