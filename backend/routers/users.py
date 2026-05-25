from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

import models
import schemas
from core.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


class UserStatusUpdate(BaseModel):
    daily_status: str


@router.get("/looking", response_model=List[schemas.UserResponse])
def get_looking_users(db: Session = Depends(get_db)):
    """Retrieve all users whose daily status is 'Looking'."""
    users = db.query(models.User).filter(models.User.daily_status == "Looking").all()
    return users


@router.patch("/{user_id}/status", response_model=schemas.UserResponse)
def update_user_status(
    user_id: int, status_update: UserStatusUpdate, db: Session = Depends(get_db)
):
    """Update a specific user's daily status."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.daily_status = status_update.daily_status
    db.commit()
    db.refresh(user)
    return user
