from models import User, Group


def test_create_group(client):
    response = client.post("/groups", json={"is_locked": False})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["is_locked"] is False


def test_join_group(client, db_session):
    group = Group()
    db_session.add(group)
    user = User(email="joiner@test.com", name="Joiner", daily_status="Looking")
    db_session.add(user)
    db_session.commit()

    response = client.post(f"/groups/{group.id}/join", json={"user_id": user.id})
    assert response.status_code == 200
    assert response.json()["user_id"] == user.id


def test_join_group_not_looking_fails(client, db_session):
    group = Group()
    db_session.add(group)
    user = User(email="busy@test.com", name="Busy", daily_status="Not Looking")
    db_session.add(user)
    db_session.commit()

    response = client.post(f"/groups/{group.id}/join", json={"user_id": user.id})
    assert response.status_code == 400
    assert "status must be 'Looking'" in response.json()["detail"]


def test_join_group_locked_fails(client, db_session):
    group = Group(is_locked=True)
    db_session.add(group)
    user = User(email="late@test.com", name="Late", daily_status="Looking")
    db_session.add(user)
    db_session.commit()

    response = client.post(f"/groups/{group.id}/join", json={"user_id": user.id})
    assert response.status_code == 400
    assert "finalized and locked" in response.json()["detail"]
