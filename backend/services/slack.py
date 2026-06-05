from slack_sdk import WebClient
from core.config import settings

client = WebClient(token=settings.slack_bot_token)
