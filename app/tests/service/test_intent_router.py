import uuid
from unittest.mock import MagicMock

import pytest

from app.core.story import Story
from app.core.user_intent import UserIntent, maybe_play_story
from app.service.intent_router import SemanticRouteResult, route, keywords_check_intent
from app.core.conversation_message import Message, MessageType


@pytest.fixture
def mock_get_message_service(monkeypatch):
    mock_service = MagicMock()

    monkeypatch.setattr("app.service.intent_router.get_message_service", lambda: mock_service)

    return mock_service


def test_get_user_intent(mock_get_message_service):
    mock_get_message_service.get_latest_current_user_and_role_messages.return_value = []

    assert keywords_check_intent("我想听一个故事") == UserIntent.MAYBE_PLAY_STORY
    assert keywords_check_intent("你今天做了什么？") == UserIntent.CONVERSATION
    assert keywords_check_intent("给我放一本绘本") == UserIntent.MAYBE_PLAY_STORY
    assert keywords_check_intent("让我们讲个笑话吧") == UserIntent.MAYBE_PLAY_STORY
    assert keywords_check_intent("读一本书吧") == UserIntent.MAYBE_PLAY_STORY


def test_route_given_conversation_input(mock_get_message_service):
    mock_get_message_service.get_latest_current_user_and_role_messages.return_value = []

    result = route("你们今天为什么没有执行任务")

    assert result == SemanticRouteResult(user_intent=UserIntent.CONVERSATION)
    assert maybe_play_story() is False


def test_route_given_input_with_play_story_keywords(mock_get_message_service):
    mock_get_message_service.get_latest_current_user_and_role_messages.return_value = []

    result = route("有什么故事分享")
    print(result)
    assert result.user_intent == UserIntent.MAYBE_PLAY_STORY
    assert result.arguments is not None
    assert 'output_text' in result.arguments
    assert maybe_play_story() is True


def test_route_given_input_with_play_story_keywords_and_want_to_play_story(mock_get_message_service):
    mock_get_message_service.get_latest_current_user_and_role_messages.return_value = []

    result = route("想听故事")
    print(result)
    assert result.user_intent == UserIntent.MAYBE_PLAY_STORY
    assert result.arguments is not None
    assert 'output_text' in result.arguments
    assert maybe_play_story() is True


def test_route_given_input_with_play_story_keywords_and_story_name(mock_get_message_service):
    mock_get_message_service.get_latest_current_user_and_role_messages.return_value = []

    result = route("听小野雁")
    print(result)
    assert result.user_intent == UserIntent.PLAY_STORY
    assert result.arguments is not None
    assert 'story' in result.arguments
    assert isinstance(result.arguments["story"], Story)
    assert result.arguments["story"].name == "走失的小野雁"
    assert maybe_play_story() is False


def test_route_given_story_name_but_without_play_story_keywords(mock_get_message_service):
    mock_get_message_service.get_latest_current_user_and_role_messages.return_value = []

    result = route("走失的小野雁")

    assert result == SemanticRouteResult(user_intent=UserIntent.CONVERSATION)
    assert maybe_play_story() is False


def test_route_given_input_story_name_when_maybe_play_story(monkeypatch, mock_get_message_service):
    monkeypatch.setattr("app.service.intent_router.maybe_play_story", lambda: True)

    user_id = uuid.uuid4()
    history_messages = [
        Message(user_id=user_id, role_code=1, content="想听故事", message_type=MessageType.USER_MESSAGE),
        Message(user_id=user_id, role_code=1, content="想听什么故事啊", message_type=MessageType.ASSISTANT_MESSAGE),
    ]
    mock_get_message_service.get_latest_current_user_and_role_messages.return_value = history_messages

    result = route("小野雁")

    assert result.user_intent == UserIntent.PLAY_STORY
    assert result.arguments is not None
    assert 'story' in result.arguments
    assert isinstance(result.arguments["story"], Story)
    assert result.arguments["story"].name == "走失的小野雁"
    assert maybe_play_story() is False


def test_route_given_input_not_related_story_name_when_maybe_play_story(mock_get_message_service):
    mock_get_message_service.get_latest_current_user_and_role_messages.return_value = []

    user_id = uuid.uuid4()
    history_messages = [
        Message(user_id=user_id, role_code=1, content="想听故事", message_type=MessageType.USER_MESSAGE),
        Message(user_id=user_id, role_code=1, content="想听什么故事啊", message_type=MessageType.ASSISTANT_MESSAGE),
    ]
    mock_get_message_service.get_latest_current_user_and_role_messages.return_value = history_messages

    result = route("大灰狼")

    assert result.user_intent == UserIntent.CONVERSATION
    assert maybe_play_story() is False


def test_route_given_input_not_related_story_name(mock_get_message_service):
    mock_get_message_service.get_latest_current_user_and_role_messages.return_value = []

    result = route("听小白兔的故事")

    assert result.user_intent == UserIntent.CONVERSATION
    assert maybe_play_story() is False


def test_route_given_input_play_story_keywords_but_not_mean_want_to_play_again_and_previous_history_with_story(
        mock_get_message_service):
    user_id = uuid.uuid4()
    history_messages = [
        Message(user_id=user_id, role_code=1, content="想听大灰狼故事", message_type=MessageType.USER_MESSAGE),
        Message(user_id=user_id, role_code=1,
                content="从前大灰狼肚子空空的，导出找好吃的，最后找到羊阿姨，羊阿姨做了很多好吃的，大灰狼舍不得吃羊阿姨，最后跟羊阿姨做了好朋友。这个故事好不好听啊",
                message_type=MessageType.ASSISTANT_MESSAGE),
    ]
    mock_get_message_service.get_latest_current_user_and_role_messages.return_value = history_messages

    result = route("好听")

    assert result.user_intent == UserIntent.CONVERSATION
    assert maybe_play_story() is False
