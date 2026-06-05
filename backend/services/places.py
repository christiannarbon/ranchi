import httpx
import logging
from core.config import settings

logger = logging.getLogger(__name__)


async def search_nearby_restaurants(query: str) -> list[dict]:
    """
    Mocks a Google Places API response.
    Returns a static list of 3-4 dicts containing name, address, and place_id.
    """
    _mock_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={settings.google_places_api_key}"

    try:
        # In a real implementation:
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(_mock_url)
        #     response.raise_for_status()
        #     return response.json().get("results", [])

        # Simulating httpx library usage with mocked static data
        mocked_results = [
            {
                "name": "The Rusty Spoon",
                "address": "123 Main St, Cityville",
                "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
            },
            {
                "name": "Pasta Paradise",
                "address": "456 Oak Ave, Cityville",
                "place_id": "ChIJyWEHuEmuEmsRm9hTkapTCrk",
            },
            {
                "name": "Burger Barn",
                "address": "789 Pine Ln, Cityville",
                "place_id": "ChIJd8BlQ2BZwokRAFUEcm_qrcA",
            },
            {
                "name": "Sushi Central",
                "address": "321 Cedar Blvd, Cityville",
                "place_id": "ChIJrTLr-GyuEmsRBfy61i59si0",
            },
        ]

        return mocked_results

    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting {exc.request.url!r}.")
        raise Exception("External API request failed") from exc
    except httpx.HTTPStatusError as exc:
        logger.error(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
        )
        raise Exception("External API returned an error") from exc
