from models import User


def test_get_looking_users_empty(client):
    response = client.get("/users/looking")
    assert response.status_code == 200
    assert response.json() == []


def test_register_success(client):
    response = client.post(
        "/users/register", json={"email": "new@example.com", "name": "New User"}
    )
    assert response.status_code == 201
    assert "api_token" in response.json()
    assert response.json()["email"] == "new@example.com"


def test_register_duplicate_email(client):
    client.post(
        "/users/register", json={"email": "new@example.com", "name": "New User"}
    )
    response = client.post(
        "/users/register", json={"email": "new@example.com", "name": "Another User"}
    )
    assert response.status_code == 409


def test_get_me_valid_token(client, db_session):
    user = User(email="test@example.com", name="Test User", api_token="secret-token")
    db_session.add(user)
    db_session.commit()
    response = client.get("/users/me", headers={"Authorization": "Bearer secret-token"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_get_me_invalid_token(client):
    response = client.get("/users/me", headers={"Authorization": "Bearer bad-token"})
    assert response.status_code == 401


def test_get_me_missing_header(client):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_update_status_success(client, db_session):
    user = User(email="test@example.com", name="Test User", api_token="secret-token")
    db_session.add(user)
    db_session.commit()
    response = client.patch(
        f"/users/{user.id}/status",
        json={"daily_status": "Looking"},
        headers={"Authorization": "Bearer secret-token"},
    )
    assert response.status_code == 200
    assert response.json()["daily_status"] == "Looking"


def test_update_status_wrong_user(client, db_session):
    user1 = User(email="test1@example.com", name="User 1", api_token="token1")
    user2 = User(email="test2@example.com", name="User 2", api_token="token2")
    db_session.add_all([user1, user2])
    db_session.commit()
    response = client.patch(
        f"/users/{user2.id}/status",
        json={"daily_status": "Looking"},
        headers={"Authorization": "Bearer token1"},
    )
    assert response.status_code == 403


def test_update_status_invalid_value(client, db_session):
    user = User(email="test@example.com", name="Test User", api_token="secret-token")
    db_session.add(user)
    db_session.commit()
    response = client.patch(
        f"/users/{user.id}/status",
        json={"daily_status": "Partying"},
        headers={"Authorization": "Bearer secret-token"},
    )
    assert response.status_code == 422
