import datetime
import uuid

import pytest
from core.role import Role
from core.conversation_message import Message, MessageType, get_current_role_messages, save_message, messages, get_conversation_history

@pytest.fixture(autouse=True)
def clear_messages():
    """每个测试运行前自动清空全局 messages 列表"""
    messages.clear()

def test_save_message():
    test_message = Message(
        role_code=1,
        content="Hello, this is a test message.",
        message_type=MessageType.USER_MESSAGE,
    )

    saved_message = save_message(test_message)

    assert type(saved_message) is Message
    assert saved_message.id is not None
    assert type(saved_message.id) is uuid.UUID
    assert saved_message.created_time is not None
    assert type(saved_message.created_time) is datetime.datetime
    assert saved_message.content == "Hello, this is a test message."
    assert saved_message.message_type == MessageType.USER_MESSAGE
    assert len(messages) == 1
    assert messages[0]["id"] == saved_message.id

def test_get_conversation_history():
    history = get_conversation_history(role_code=1, round=1)
    assert len(history) == 0

    user_message1 = Message(
        role_code=1,
        content="Hello, this is a user message 1",
        message_type=MessageType.USER_MESSAGE,
    )
    assistant_message1 = Message(
        role_code=1,
        content="Hello, this is a assistant message 1",
        message_type=MessageType.ASSISTANT_MESSAGE,
        parent_id=user_message1.id
    )
    user_message2 = Message(
        role_code=1,
        content="Hello, this is a user message 2",
        message_type=MessageType.USER_MESSAGE,
        parent_id=assistant_message1.id
    )
    save_message(user_message1)
    save_message(assistant_message1)
    save_message(user_message2)

    history = get_conversation_history(role_code=1, round=1)
    assert len(history) == 1
    assert len(history[0]) == 2
    assert history[0][0] == user_message1.content
    assert history[0][1] == assistant_message1.content

    assistant_message2 = Message(
        role_code=1,
        content="Hello, this is a assistant message 2",
        message_type=MessageType.ASSISTANT_MESSAGE,
        parent_id=user_message2.id
    )
    save_message(assistant_message2)

    history = get_conversation_history(role_code=1, round=1)
    assert len(history) == 1
    assert len(history[0]) == 2
    assert history[0][0] == user_message2.content
    assert history[0][1] == assistant_message2.content


def test_get_current_role_messages(monkeypatch):
    mock_role = {
        "code": 1,
        "name": "Test Role",
        "prompt": "Test Prompt",
        "voice_name": "Test Voice",
        "voice_type": "Test Voice Type",
        "self_introduction": "Test Introduction",
        "self_introduction_voice": "Test Introduction Voice",
        "retry_voice": "Test Retry Voice",
    }
    monkeypatch.setattr('core.conversation_message.get_current_role', lambda: Role(**mock_role))
    
    user_message1 = Message(
        role_code=1,
        content="Hello, this is a user message 1",
        audio_id=["user_audio1"],
        message_type=MessageType.USER_MESSAGE,
    )
    assistant_message1 = Message(
        role_code=1,
        content="Hello, this is a assistant message 1",
        audio_id=["assistant_audio1", "assistant_audio2"],
        message_type=MessageType.ASSISTANT_MESSAGE,
        parent_id=user_message1.id
    )
    user_message2_role2 = Message(
        role_code=2,
        content="Hello, this is a user message 2",
        audio_id=["user_audio2"],
        message_type=MessageType.USER_MESSAGE,
        parent_id=assistant_message1.id
    )
    save_message(user_message1)
    save_message(assistant_message1)
    save_message(user_message2_role2)


    messages = get_current_role_messages()

    assert len(messages) == 2
    assert isinstance(messages[0], Message)

    messages = get_current_role_messages(last_message_num=1)

    assert len(messages) == 1
    assert messages[0].content == assistant_message1.content
    assert messages[0].audio_id == assistant_message1.audio_id

    

