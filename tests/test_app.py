from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    # Arrange: nothing special, just hit the endpoint
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # the initial fixtures defined in app.py should be present
    assert "Chess Club" in data


def test_signup_new_participant():
    # Arrange
    activity = "Chess Club"
    email = "new@student.edu"
    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]


def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert resp.status_code == 400


def test_signup_nonexistent_activity():
    # Arrange
    fake = "Nonexistent"
    email = "someone@school.edu"
    # Act
    resp = client.post(f"/activities/{fake}/signup?email={email}")
    # Assert
    assert resp.status_code == 404


def test_remove_participant():
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"
    # Act
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]


def test_remove_nonexistent_participant():
    # Arrange
    activity = "Chess Club"
    email = "not@here.edu"
    # Act
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert resp.status_code == 404
