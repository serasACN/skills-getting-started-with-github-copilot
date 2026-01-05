import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Debate Team" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Debate Team"
    # Ensure user is not already signed up
    client.post(f"/activities/{activity}/signup?email=remove_{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert f"Signed up {email} for {activity}" in data["message"]
    # Try to sign up again (should allow duplicates in current logic)
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 200

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
