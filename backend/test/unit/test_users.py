import pytest
from models import User


def test_get_looking_users_empty(client):
    response = client.get("/users/looking")
    assert response.status_code == 200
    assert response.json() == []


def test_update_user_status(client, db_session):
    # Setup user
    user = User(email="test@example.com", name="Test User", daily_status="Not Looking")
    db_session.add(user)
    db_session.commit()

    response = client.patch(
        f"/users/{user.id}/status", json={"daily_status": "Looking"}
    )
    assert response.status_code == 200
    assert response.json()["daily_status"] == "Looking"

    # Verify the GET endpoint sees them now
    response_looking = client.get("/users/looking")
    assert len(response_looking.json()) == 1
    assert response_looking.json()[0]["email"] == "test@example.com"


def test_update_user_status_not_found(client):
    response = client.patch("/users/999/status", json={"daily_status": "Looking"})
    assert response.status_code == 404
