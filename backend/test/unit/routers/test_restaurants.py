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


def test_search_returns_empty_for_zero_results(client):
    with patch("services.places.httpx.get") as mock_get:
        mock_get.return_value.json.return_value = {"status": "ZERO_RESULTS"}
        response = client.get("/restaurants/search?query=notarealplace")
    assert response.status_code == 200
    assert response.json() == []


def test_search_places_api_error(client):
    with patch("services.places.httpx.get") as mock_get:
        mock_get.return_value.json.return_value = {"status": "REQUEST_DENIED"}
        response = client.get("/restaurants/search?query=sushi")
    assert response.status_code == 503
    assert "REQUEST_DENIED" in response.json()["detail"]
