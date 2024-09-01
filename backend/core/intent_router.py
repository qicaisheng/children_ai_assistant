from core.user_intent import UserIntent


PLAY_STORY_KEYWORDS = ["听", "放", "故事", "绘本", "书", "讲"]


def keywords_rule_router(input: str):
    for keyword in PLAY_STORY_KEYWORDS:
        if keyword in input:
            return UserIntent.MAYBE_PLAY_STORY
    return UserIntent.CONVERSATION