import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
from core.database import get_db
from core.config import settings
from routers.voting import finalize_group
from slack_sdk.errors import SlackApiError
from services.slack import client
from services.slack_messages import (
    build_morning_prompt_blocks,
    build_winner_announcement_blocks,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cron", tags=["cron"])


def verify_cron_secret(authorization: str | None = Header(None)):
    """Validate Vercel Cron's Authorization: Bearer <CRON_SECRET> header."""
    expected = f"Bearer {settings.cron_secret}"
    if not authorization or authorization != expected:
        raise HTTPException(
            status_code=401, detail="Invalid or missing cron authorization"
        )


@router.get("/morning-prompt", dependencies=[Depends(verify_cron_secret)])
def morning_prompt(db: Session = Depends(get_db)):
    """Simulate sending a morning Slack prompt to all active users."""
    # Assuming all users in DB are active
    users = db.query(models.User).all()
    notified_count = 0

    for user in users:
        if not user.slack_user_id:
            logger.warning(f"User {user.id} has no slack_user_id, skipping.")
            continue

        blocks = build_morning_prompt_blocks(user_id=user.id, user_name=user.name)

        try:
            client.chat_postMessage(channel=user.slack_user_id, blocks=blocks)
            notified_count += 1
        except SlackApiError as e:
            logger.error(f"Failed to DM user {user.id}: {e.response['error']}")

    return {"status": "Morning prompts sent", "users_notified": notified_count}


@router.get("/finalize-votes", dependencies=[Depends(verify_cron_secret)])
def trigger_finalize_votes(db: Session = Depends(get_db)):
    """Find all unlocked groups created today, finalize them, and print winner to console."""
    jst = ZoneInfo("Asia/Tokyo")
    today_jst = datetime.now(jst).date()

    # Query unlocked groups created today (JST business day)
    unlocked_groups = (
        db.query(models.Group)
        .filter(
            models.Group.is_locked.is_(False),
            func.date(func.timezone("Asia/Tokyo", models.Group.created_at))
            == today_jst,
        )
        .all()
    )

    finalized_count = 0
    for group in unlocked_groups:
        try:
            # Reuse the core logic from our voting router
            finalized_group = finalize_group(group.id, db)
            finalized_count += 1

            # Determine the name of the winning restaurant
            winner_name = "No winner (no nominations)"
            if finalized_group.winning_restaurant_id:
                winner_nom = (
                    db.query(models.Nomination)
                    .filter(
                        models.Nomination.id == finalized_group.winning_restaurant_id
                    )
                    .first()
                )
                if winner_nom:
                    winner_name = winner_nom.restaurant_name

            # Notify group members
            members = (
                db.query(models.GroupMember)
                .filter(models.GroupMember.group_id == group.id)
                .all()
            )
            for member in members:
                user = (
                    db.query(models.User)
                    .filter(models.User.id == member.user_id)
                    .first()
                )
                if user:
                    if not user.slack_user_id:
                        logger.warning(
                            f"User {user.id} has no slack_user_id, skipping notification."
                        )
                        continue

                    blocks = build_winner_announcement_blocks(
                        group_id=group.id, winner_name=winner_name
                    )
                    try:
                        client.chat_postMessage(
                            channel=user.slack_user_id, blocks=blocks
                        )
                    except SlackApiError as e:
                        logger.error(
                            f"Failed to notify user {user.id}: {e.response['error']}"
                        )
                    except Exception as e:
                        logger.error(
                            f"Unexpected error notifying user {user.id}: {str(e)}"
                        )

        except HTTPException as e:
            logger.error(f"Failed to finalize group {group.id}: {e.detail}")
            db.rollback()
        except Exception as e:
            logger.error(f"Unexpected error finalizing group {group.id}: {str(e)}")
            db.rollback()

    return {"status": "Groups finalized", "groups_processed": finalized_count}
