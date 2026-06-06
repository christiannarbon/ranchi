import httpx
from core.config import settings

PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"


class PlacesAPIError(Exception):
    pass


def search_restaurants(query: str) -> list[dict]:
    response = httpx.get(
        PLACES_URL,
        params={
            "query": query,
            "type": "restaurant",
            "key": settings.google_places_api_key,
        },
    )
    data = response.json()

    if data.get("status") == "ZERO_RESULTS":
        return []

    if data.get("status") != "OK":
        raise PlacesAPIError(f"Google Places API error: {data.get('status')}")

    results = []
    for place in data.get("results", [])[:5]:
        results.append(
            {
                "name": place["name"],
                "address": place.get("formatted_address", ""),
                "place_id": place["place_id"],
            }
        )
    return results
