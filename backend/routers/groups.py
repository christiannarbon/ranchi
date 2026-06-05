from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from core.database import get_db

router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("", response_model=schemas.GroupResponse)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    """Create a new lunch group."""
    db_group = models.Group(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


@router.post("/{group_id}/join", response_model=schemas.GroupMemberResponse)
def join_group(
    group_id: int, request: schemas.JoinGroupRequest, db: Session = Depends(get_db)
):
    """Add a user to a group, enforcing constraints."""
    user_id = request.user_id

    # 1. Check if user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Check if user status is "Looking"
    if user.daily_status != "Looking":
        raise HTTPException(
            status_code=400, detail="User status must be 'Looking' to join a group"
        )

    # 3. Check if group exists
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if group.is_locked:
        raise HTTPException(
            status_code=400, detail="Cannot join: Group is finalized and locked"
        )

    # 4. Enforce group member limit (max 6 members)
    current_members = (
        db.query(models.GroupMember)
        .filter(models.GroupMember.group_id == group_id)
        .count()
    )
    if current_members >= 6:
        raise HTTPException(
            status_code=400, detail="Group already has the maximum of 6 members"
        )

    # 5. Prevent duplicate joining
    existing_member = (
        db.query(models.GroupMember)
        .filter(
            models.GroupMember.group_id == group_id,
            models.GroupMember.user_id == user_id,
        )
        .first()
    )
    if existing_member:
        raise HTTPException(status_code=400, detail="User is already in this group")

    # 6. Add user to group
    group_member = models.GroupMember(user_id=user_id, group_id=group_id)
    db.add(group_member)
    db.commit()
    db.refresh(group_member)

    return group_member
