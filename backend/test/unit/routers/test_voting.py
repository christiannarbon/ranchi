from models import User, Group


def test_nominate_restaurant(client, db_session):
    group = Group()
    db_session.add(group)
    user = User(email="n@t.com", name="N", daily_status="Looking")
    db_session.add(user)
    db_session.commit()

    # user joins group
    client.post(f"/groups/{group.id}/join", json={"user_id": user.id})

    # nominate
    response = client.post(
        f"/groups/{group.id}/nominate",
        json={"restaurant_name": "r1", "user_id": user.id},
    )
    assert response.status_code == 200
    assert response.json()["restaurant_name"] == "r1"


def test_vote_restaurant(client, db_session):
    group = Group()
    db_session.add(group)
    user = User(email="v@t.com", name="V", daily_status="Looking")
    db_session.add(user)
    db_session.commit()

    client.post(f"/groups/{group.id}/join", json={"user_id": user.id})
    nom = client.post(
        f"/groups/{group.id}/nominate",
        json={"restaurant_name": "r1", "user_id": user.id},
    ).json()

    response = client.post(
        f"/groups/{group.id}/vote",
        json={"nomination_id": nom["id"], "user_id": user.id},
    )
    assert response.status_code == 200
    assert response.json()["nomination_id"] == nom["id"]


def test_finalize_group(client, db_session):
    group = Group()
    db_session.add(group)
    user = User(email="f@t.com", name="F", daily_status="Looking")
    db_session.add(user)
    db_session.commit()

    client.post(f"/groups/{group.id}/join", json={"user_id": user.id})
    nom = client.post(
        f"/groups/{group.id}/nominate",
        json={"restaurant_name": "r1", "user_id": user.id},
    ).json()
    client.post(
        f"/groups/{group.id}/vote",
        json={"nomination_id": nom["id"], "user_id": user.id},
    )

    response = client.post(f"/groups/{group.id}/finalize")
    assert response.status_code == 200
    assert response.json()["is_locked"] is True
    assert response.json()["winning_restaurant_id"] == nom["id"]
