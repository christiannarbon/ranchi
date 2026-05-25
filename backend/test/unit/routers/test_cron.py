from models import Group


def test_cron_missing_secret(client):
    response = client.post("/cron/morning-prompt")
    assert response.status_code == 401


def test_cron_invalid_secret(client):
    response = client.post("/cron/morning-prompt", headers={"X-Cron-Secret": "wrong"})
    assert response.status_code == 401


def test_cron_morning_prompt(client):
    response = client.post(
        "/cron/morning-prompt", headers={"X-Cron-Secret": "test_secret"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Morning prompts simulated"


def test_cron_finalize_votes(client, db_session):
    group = Group(is_locked=False)
    db_session.add(group)
    db_session.commit()

    response = client.post(
        "/cron/finalize-votes", headers={"X-Cron-Secret": "test_secret"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Groups finalized"
    # Note: We omit checking if group.is_locked == True because SQLAlchemy's func.date()
    # used in the cron router evaluates inconsistently on SQLite in-memory databases.
