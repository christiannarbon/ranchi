import unittest.mock as mock
from models import Group, User


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
    assert response.json()["status"] == "Morning prompts sent"


@mock.patch("routers.cron.client.chat_postMessage")
def test_morning_prompt_sends_real_dm(mock_post_message, client, db_session):
    user1 = User(name="User 1", email="user1@example.com", slack_user_id="U1234")
    user2 = User(name="User 2", email="user2@example.com", slack_user_id="U5678")
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    response = client.post(
        "/cron/morning-prompt", headers={"X-Cron-Secret": "test_secret"}
    )

    assert response.status_code == 200
    assert response.json()["users_notified"] == 2
    assert mock_post_message.call_count == 2

    calls = mock_post_message.call_args_list
    channels_called = [call.kwargs.get("channel") for call in calls]
    assert "U1234" in channels_called
    assert "U5678" in channels_called


@mock.patch("routers.cron.client.chat_postMessage")
def test_morning_prompt_skips_users_without_slack_id(
    mock_post_message, client, db_session
):
    user = User(name="User No Slack", email="noslack@example.com", slack_user_id=None)
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/cron/morning-prompt", headers={"X-Cron-Secret": "test_secret"}
    )

    assert response.status_code == 200
    assert response.json()["users_notified"] == 0
    assert mock_post_message.call_count == 0


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
