import json
from unittest import mock
import pytest
from models import User


@pytest.fixture
def mock_valid_signature():
    with mock.patch("routers.slack.SignatureVerifier.is_valid_request") as mock_verify:
        mock_verify.return_value = True
        yield mock_verify


def test_interactions_invalid_signature(client):
    with mock.patch("routers.slack.SignatureVerifier.is_valid_request") as mock_verify:
        mock_verify.return_value = False
        response = client.post(
            "/slack/interactions",
            headers={
                "X-Slack-Signature": "v0=invalid",
                "X-Slack-Request-Timestamp": "1234567890",
            },
            data="payload={}",
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid Slack signature"}


def test_interactions_sets_status_looking(client, db_session, mock_valid_signature):
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    payload = {
        "actions": [
            {"action_id": "set_status_looking", "value": f"{user.id}:status_looking"}
        ]
    }

    response = client.post(
        "/slack/interactions",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"payload": json.dumps(payload)},
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}

    db_session.refresh(user)
    assert user.daily_status == "Looking"


def test_interactions_sets_status_solo(client, db_session, mock_valid_signature):
    user = User(name="Test User", email="test2@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    payload = {
        "actions": [{"action_id": "set_status_skip", "value": f"{user.id}:status_skip"}]
    }

    response = client.post(
        "/slack/interactions",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"payload": json.dumps(payload)},
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}

    db_session.refresh(user)
    assert user.daily_status == "Solo"


def test_interactions_unknown_user(client, mock_valid_signature):
    payload = {
        "actions": [{"action_id": "set_status_looking", "value": "9999:status_looking"}]
    }

    response = client.post(
        "/slack/interactions",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"payload": json.dumps(payload)},
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}


@mock.patch("routers.slack.client.chat_postEphemeral")
def test_interactions_unknown_action_id(
    mock_post_ephemeral, client, db_session, mock_valid_signature
):
    user = User(name="Test User", email="test3@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    payload = {
        "channel": {"id": "C12345"},
        "user": {"id": "U12345"},
        "actions": [
            {"action_id": "some_future_action", "value": f"{user.id}:something"}
        ],
    }

    response = client.post(
        "/slack/interactions",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"payload": json.dumps(payload)},
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}

    db_session.refresh(user)
    assert user.daily_status is None

    mock_post_ephemeral.assert_called_once_with(
        channel="C12345",
        user="U12345",
        text="Sorry, this button is no longer active or is unrecognized.",
    )
