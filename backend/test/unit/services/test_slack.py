def test_slack_client_uses_configured_token():
    from services.slack import client

    assert client.token == "test_token"
