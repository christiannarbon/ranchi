from slack_sdk import WebClient
from core.database import settings

client = WebClient(token=settings.slack_bot_token)
