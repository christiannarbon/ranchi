from fastapi import APIRouter, Query, HTTPException
from services.places import search_restaurants

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("/search")
def search(query: str = Query(..., min_length=2)):
    """Search for restaurants by name. Requires Google Places API key (Epic 3)."""
    try:
        return search_restaurants(query)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
