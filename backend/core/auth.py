from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
import models
from core.database import get_db


def get_current_user(
    authorization: str | None = Header(None), db: Session = Depends(get_db)
) -> models.User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Missing or invalid Authorization header"
        )
    token = authorization.removeprefix("Bearer ").strip()
    user = db.query(models.User).filter(models.User.api_token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
