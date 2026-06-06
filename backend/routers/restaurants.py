from fastapi import APIRouter, Query, HTTPException
from services.places import search_restaurants, PlacesAPIError

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("/search")
def search(query: str = Query(..., min_length=2)):
    try:
        return search_restaurants(query)
    except PlacesAPIError as e:
        raise HTTPException(status_code=503, detail=str(e))
