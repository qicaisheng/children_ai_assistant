from core.user_intent import check_user_intent, UserIntent


def test_get_user_intent():
    assert check_user_intent("我想听一个故事") == UserIntent.MAYBE_PLAY_STORY
    assert check_user_intent("你今天做了什么？") == UserIntent.CONVERSATION
    assert check_user_intent("给我放一本绘本") == UserIntent.MAYBE_PLAY_STORY
    assert check_user_intent("让我们讲个笑话吧") == UserIntent.MAYBE_PLAY_STORY
    assert check_user_intent("读一本书吧") == UserIntent.MAYBE_PLAY_STORY