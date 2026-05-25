from fastapi import APIRouter, HTTPException, Query
from typing import List
from pydantic import BaseModel

from services.places import search_nearby_restaurants

router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"]
)

class RestaurantResponse(BaseModel):
    name: str
    address: str
    place_id: str

@router.get("/search", response_model=List[RestaurantResponse])
async def search_restaurants(query: str = Query(..., description="Search query for restaurants")):
    """
    Search for nearby restaurants based on a query string.
    Currently returns mocked static data.
    """
    try:
        results = await search_nearby_restaurants(query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch restaurant data from external service.")
