def test_search_restaurants(client):
    response = client.get("/restaurants/search?query=pizza")
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) > 0
    assert "place_id" in results[0]
