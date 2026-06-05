from unittest.mock import patch


def test_search_returns_results(client):
    mock_results = [
        {"name": "Sushi Place", "address": "1 Main St", "place_id": "abc123"},
    ]
    with patch("routers.restaurants.search_restaurants", return_value=mock_results):
        response = client.get("/restaurants/search?query=sushi")
    assert response.status_code == 200
    assert response.json() == mock_results


def test_search_query_too_short(client):
    response = client.get("/restaurants/search?query=s")
    assert response.status_code == 422  # FastAPI validation


def test_search_not_implemented(client):
    with patch(
        "routers.restaurants.search_restaurants",
        side_effect=NotImplementedError("Not ready"),
    ):
        response = client.get("/restaurants/search?query=ramen")
    assert response.status_code == 501
    assert "Not ready" in response.json()["detail"]
