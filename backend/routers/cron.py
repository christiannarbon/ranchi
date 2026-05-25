import json
import logging
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
from core.database import get_db, settings
from routers.voting import finalize_group

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/cron",
    tags=["cron"]
)

def verify_cron_secret(x_cron_secret: str | None = Header(None)):
    """Dependency to check the X-Cron-Secret header against the server settings."""
    if not x_cron_secret or x_cron_secret != settings.cron_secret:
        raise HTTPException(status_code=401, detail="Invalid or missing X-Cron-Secret header")

@router.post("/morning-prompt", dependencies=[Depends(verify_cron_secret)])
def morning_prompt(db: Session = Depends(get_db)):
    """Simulate sending a morning Slack prompt to all active users."""
    # Assuming all users in DB are active
    users = db.query(models.User).all()
    
    for user in users:
        # Simulate Slack Block Kit payload
        slack_payload = {
            "channel": user.email, # simulating a DM using email as identifier
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Good morning {user.name}! Are you looking for a lunch group today?"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Yes, I'm looking"},
                            "value": "status_looking",
                            "action_id": "set_status_looking"
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "No, skip me"},
                            "value": "status_skip",
                            "action_id": "set_status_skip"
                        }
                    ]
                }
            ]
        }
        
        # Print the structured JSON to standard output as per requirements
        print(f"\\n--- SLACK PAYLOAD (MORNING PROMPT) FOR {user.email} ---")
        print(json.dumps(slack_payload, indent=2))
        
    return {"status": "Morning prompts simulated", "users_notified": len(users)}

@router.post("/finalize-votes", dependencies=[Depends(verify_cron_secret)])
def trigger_finalize_votes(db: Session = Depends(get_db)):
    """Find all unlocked groups created today, finalize them, and print winner to console."""
    today = date.today()
    
    # Query unlocked groups created today
    unlocked_groups = db.query(models.Group).filter(
        models.Group.is_locked == False,
        func.date(models.Group.created_at) == today
    ).all()
    
    finalized_count = 0
    for group in unlocked_groups:
        try:
            # Reuse the core logic from our voting router
            finalized_group = finalize_group(group.id, db)
            finalized_count += 1
            
            # Determine the name of the winning restaurant
            winner_name = "No winner (no nominations)"
            if finalized_group.winning_restaurant_id:
                winner_nom = db.query(models.Nomination).filter(
                    models.Nomination.id == finalized_group.winning_restaurant_id
                ).first()
                if winner_nom:
                    winner_name = winner_nom.restaurant_name
            
            # Notify group members
            members = db.query(models.GroupMember).filter(models.GroupMember.group_id == group.id).all()
            for member in members:
                user = db.query(models.User).filter(models.User.id == member.user_id).first()
                if user:
                    slack_payload = {
                        "channel": user.email,
                        "blocks": [
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": f"Lunch Group #{group.id} finalized! The winning restaurant is: *{winner_name}*"
                                }
                            }
                        ]
                    }
                    print(f"\\n--- SLACK PAYLOAD (WINNER ANNOUNCEMENT) FOR {user.email} ---")
                    print(json.dumps(slack_payload, indent=2))
                    
        except HTTPException as e:
            logger.error(f"Failed to finalize group {group.id}: {e.detail}")
            
    return {"status": "Groups finalized", "groups_processed": finalized_count}
