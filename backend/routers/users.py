from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from core.database import get_db
from core.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register_user(
    user_create: schemas.UserCreate, response: Response, db: Session = Depends(get_db)
):
    existing = (
        db.query(models.User).filter(models.User.email == user_create.email).first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = models.User(
        email=user_create.email,
        name=user_create.name,
        daily_status=user_create.daily_status,
        slack_user_id=user_create.slack_user_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/me", response_model=schemas.UserPublicResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.get("/looking", response_model=List[schemas.UserLookingResponse])
def get_looking_users(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve all users whose daily status is 'Looking'."""
    users = db.query(models.User).filter(models.User.daily_status == "Looking").all()
    return users


@router.patch("/{user_id}/status", response_model=schemas.UserPublicResponse)
def update_status(
    user_id: int,
    body: schemas.StatusUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403, detail="Cannot update another user's status"
        )
    current_user.daily_status = body.daily_status
    db.commit()
    db.refresh(current_user)
    return current_user
