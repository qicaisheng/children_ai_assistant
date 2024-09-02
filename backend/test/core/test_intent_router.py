from core.user_intent import UserIntent, maybe_play_story
from core.intent_router import SemanticRouteResult, route
from core.conversation_message import Message, MessageType


def test_route_given_conversation_input():
    result = route("你们今天为什么没有执行任务")
    
    assert result == SemanticRouteResult(user_intent=UserIntent.CONVERSATION)
    assert maybe_play_story() is False


def test_route_given_input_with_play_story_keywords():
    result = route("有什么故事分享")
    print(result)
    assert result.user_intent == UserIntent.MAYBE_PLAY_STORY
    assert result.arguments is not None
    assert 'output_text' in result.arguments
    assert maybe_play_story() is True

def test_route_given_input_with_play_story_keywords_and_story_name():
    result = route("听小野雁")
    print(result)
    assert result.user_intent == UserIntent.PLAY_STORY
    assert result.arguments is not None
    assert 'story' in result.arguments
    assert result.arguments["story"] == "走失的小野雁"
    assert maybe_play_story() is False

def test_route_given_story_name_but_without_play_story_keywords():
    result = route("走失的小野雁")
    
    assert result == SemanticRouteResult(user_intent=UserIntent.CONVERSATION)
    assert maybe_play_story() is False

def test_route_given_input_story_name_when_maybe_play_story(monkeypatch):
    monkeypatch.setattr("core.intent_router.maybe_play_story", lambda: True)

    history_messages = [
        Message(role_code=1, content="想听故事", message_type=MessageType.USER_MESSAGE, audio_id=None),
        Message(role_code=1, content="想听什么故事啊", message_type=MessageType.ASSISTANT_MESSAGE, audio_id=None),
    ]
    monkeypatch.setattr("core.intent_router.get_current_role_messages", lambda last_message_num: history_messages)

    result = route("小野雁")

    assert result.user_intent == UserIntent.PLAY_STORY
    assert result.arguments is not None
    assert 'story' in result.arguments
    assert result.arguments["story"] == "走失的小野雁"
    assert maybe_play_story() is False

    
    


