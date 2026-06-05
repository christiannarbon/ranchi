from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import random

import models
import schemas
from core.database import get_db

router = APIRouter(prefix="/groups", tags=["voting"])


@router.post("/{group_id}/nominate", response_model=schemas.NominationResponse)
def nominate(
    group_id: int, request: schemas.NominateRequest, db: Session = Depends(get_db)
):
    """Nominate a restaurant for a group."""
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if group.is_locked:
        raise HTTPException(
            status_code=400, detail="Cannot nominate: Group is finalized and locked"
        )

    # Check if user is a member of the group
    is_member = (
        db.query(models.GroupMember)
        .filter(
            models.GroupMember.group_id == group_id,
            models.GroupMember.user_id == request.user_id,
        )
        .first()
    )
    if not is_member:
        raise HTTPException(status_code=400, detail="Only group members can nominate")

    # Enforce max 3 nominations
    current_nominations = (
        db.query(models.Nomination)
        .filter(models.Nomination.group_id == group_id)
        .count()
    )
    if current_nominations >= 3:
        raise HTTPException(
            status_code=400, detail="Group already has the maximum of 3 nominations"
        )

    # Prevent duplicate nominations in the same group
    existing_nom = (
        db.query(models.Nomination)
        .filter(
            models.Nomination.group_id == group_id,
            models.Nomination.restaurant_name == request.restaurant_name,
        )
        .first()
    )
    if existing_nom:
        raise HTTPException(
            status_code=400,
            detail="This restaurant has already been nominated in this group",
        )

    nomination = models.Nomination(
        group_id=group_id,
        restaurant_name=request.restaurant_name,
        google_place_id=request.google_place_id,
    )
    db.add(nomination)
    db.commit()
    db.refresh(nomination)
    return nomination


@router.post("/{group_id}/vote", response_model=schemas.VoteResponse)
def vote(group_id: int, request: schemas.VoteRequest, db: Session = Depends(get_db)):
    """Vote for a specific nomination in the group."""
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if group.is_locked:
        raise HTTPException(
            status_code=400, detail="Cannot vote: Group is finalized and locked"
        )

    # Check if user is a member of the group
    is_member = (
        db.query(models.GroupMember)
        .filter(
            models.GroupMember.group_id == group_id,
            models.GroupMember.user_id == request.user_id,
        )
        .first()
    )
    if not is_member:
        raise HTTPException(status_code=400, detail="Only group members can vote")

    # Verify the nomination belongs to this group
    nomination = (
        db.query(models.Nomination)
        .filter(
            models.Nomination.id == request.nomination_id,
            models.Nomination.group_id == group_id,
        )
        .first()
    )
    if not nomination:
        raise HTTPException(
            status_code=404, detail="Nomination not found in this group"
        )

    # A user can only vote once per group
    existing_vote = (
        db.query(models.Vote)
        .join(models.Nomination)
        .filter(
            models.Vote.user_id == request.user_id,
            models.Nomination.group_id == group_id,
        )
        .first()
    )
    if existing_vote:
        raise HTTPException(
            status_code=400, detail="User has already voted in this group"
        )

    vote = models.Vote(user_id=request.user_id, nomination_id=request.nomination_id)
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return vote


@router.post("/{group_id}/finalize", response_model=schemas.GroupResponse)
def finalize_group(group_id: int, db: Session = Depends(get_db)):
    """Tally votes, assign the winning restaurant, and lock the group."""
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if group.is_locked:
        raise HTTPException(status_code=400, detail="Group is already finalized")

    # Tally votes for nominations in this group
    vote_counts = (
        db.query(
            models.Vote.nomination_id, func.count(models.Vote.id).label("vote_count")
        )
        .join(models.Nomination)
        .filter(models.Nomination.group_id == group_id)
        .group_by(models.Vote.nomination_id)
        .all()
    )

    if not vote_counts:
        # If no votes, either pick a random nomination or leave it None
        nominations = (
            db.query(models.Nomination)
            .filter(models.Nomination.group_id == group_id)
            .all()
        )
        if nominations:
            winner = random.choice(nominations)
            group.winning_restaurant_id = winner.id
    else:
        # Find the max vote count
        max_votes = max(vc.vote_count for vc in vote_counts)
        # Handle ties by collecting all nominations with max votes
        tied_nominations = [
            vc.nomination_id for vc in vote_counts if vc.vote_count == max_votes
        ]

        # Pick winner randomly among ties
        winning_nomination_id = random.choice(tied_nominations)
        group.winning_restaurant_id = winning_nomination_id

    # Lock the group
    group.is_locked = True
    db.commit()
    db.refresh(group)
    return group
