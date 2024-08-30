
from enum import Enum


class UserIntent(Enum):
    MAYBE_PLAY_STORY = "MAYBE_PLAY_STORY",
    CONVERSATION = "CONVERSATION",

PLAY_STORY_KEYWORDS = ["听", "放", "故事", "绘本", "书", "讲"]

def check_user_intent(input: str) -> UserIntent:
    for keyword in PLAY_STORY_KEYWORDS:
        if keyword in input:
            return UserIntent.MAYBE_PLAY_STORY
    return UserIntent.CONVERSATION