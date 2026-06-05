def build_morning_prompt_blocks(user_id: int, user_name: str) -> list[dict]:
    """Build the Slack Block Kit blocks for the morning lunch prompt DM."""
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Good morning {user_name}! Are you looking for a lunch group today?",
            },
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Yes, I'm looking"},
                    "value": f"{user_id}:status_looking",
                    "action_id": "set_status_looking",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "No, skip me"},
                    "value": f"{user_id}:status_skip",
                    "action_id": "set_status_skip",
                },
            ],
        },
    ]


def build_winner_announcement_blocks(group_id: int, winner_name: str) -> list[dict]:
    """Build the Slack Block Kit blocks for the winner announcement DM."""
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Lunch Group #{group_id} finalized! The winning restaurant is: *{winner_name}*",
            },
        }
    ]
