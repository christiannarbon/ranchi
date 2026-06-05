from services.slack_messages import (
    build_morning_prompt_blocks,
    build_winner_announcement_blocks,
)


def test_morning_prompt_blocks_structure():
    blocks = build_morning_prompt_blocks(user_id=42, user_name="Alice")
    assert len(blocks) == 2
    assert blocks[0]["type"] == "section"
    assert "Alice" in blocks[0]["text"]["text"]
    assert blocks[1]["type"] == "actions"
    elements = blocks[1]["elements"]
    assert len(elements) == 2
    assert elements[0]["value"] == "42:status_looking"
    assert elements[0]["action_id"] == "set_status_looking"
    assert elements[1]["value"] == "42:status_skip"
    assert elements[1]["action_id"] == "set_status_skip"


def test_winner_announcement_blocks_structure():
    blocks = build_winner_announcement_blocks(group_id=7, winner_name="Sushi Central")
    assert len(blocks) == 1
    assert blocks[0]["type"] == "section"
    text = blocks[0]["text"]["text"]
    assert "7" in text
    assert "Sushi Central" in text
