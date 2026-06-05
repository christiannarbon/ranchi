import json
import logging
from urllib.parse import parse_qsl

from fastapi import APIRouter, Request, HTTPException, Depends
from slack_sdk.signature import SignatureVerifier
from sqlalchemy.orm import Session

import models
from core.database import get_db
from core.config import settings
from services.slack import client
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/slack", tags=["slack"])


def get_signature_verifier() -> SignatureVerifier:
    return SignatureVerifier(settings.slack_signing_secret)


@router.post("/interactions")
async def slack_interactions(
    request: Request,
    db: Session = Depends(get_db),
    verifier: SignatureVerifier = Depends(get_signature_verifier),
):
    body = await request.body()

    if not verifier.is_valid_request(body=body, headers=dict(request.headers)):
        raise HTTPException(status_code=401, detail="Invalid Slack signature")

    form_data = dict(parse_qsl(body.decode("utf-8")))
    payload_str = form_data.get("payload")
    if not payload_str:
        return {"ok": True}

    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        return {"ok": True}

    actions = payload.get("actions", [])
    if not actions:
        return {"ok": True}

    action = actions[0]
    action_id = action.get("action_id")
    value = action.get("value")

    if not value or ":" not in value:
        return {"ok": True}

    try:
        user_id = int(value.split(":")[0])
    except ValueError:
        return {"ok": True}

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.warning(f"Slack interaction received for unknown user ID {user_id}")
        return {"ok": True}

    if action_id == "set_status_looking":
        user.daily_status = "Looking"
    elif action_id == "set_status_skip":
        user.daily_status = "Solo"
    else:
        logger.warning(f"Unrecognised action_id received from Slack: {action_id!r}")
        channel_id = payload.get("channel", {}).get("id")
        slack_user_id = payload.get("user", {}).get("id")
        if channel_id and slack_user_id:
            try:
                client.chat_postEphemeral(
                    channel=channel_id,
                    user=slack_user_id,
                    text="Sorry, this button is no longer active or is unrecognized.",
                )
            except SlackApiError as e:
                logger.error(f"Failed to send ephemeral error: {e.response['error']}")
        return {"ok": True}

    db.commit()

    return {"ok": True}
