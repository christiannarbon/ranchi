import logging

logger = logging.getLogger(__name__)


def search_restaurants(query: str) -> list[dict]:
    """
    Search for restaurants matching the given query via Google Places API.

    TODO (Epic 3): Implement real Google Places Text Search API call using httpx.
    Reference: https://developers.google.com/maps/documentation/places/web-service/text-search
    """
    raise NotImplementedError(
        "Google Places search is not yet implemented. See Epic 3 — Restaurant Search."
    )
