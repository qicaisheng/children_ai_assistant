import uuid

import pytest
from unittest.mock import patch, MagicMock

from app.core.conversation_message import Message, MessageType
from app.service.conversation_service import build_llm_request_message, get_conversation_history


@pytest.fixture
def mock_get_system_prompt_by_role_code(monkeypatch):
    def mock_prompt(role_code):
        return "Mocked System Prompt"
    monkeypatch.setattr("app.service.conversation_service.get_system_prompt_by_role_code", mock_prompt)

@pytest.fixture
def mock_get_conversation_history(monkeypatch):
    def mock_history(role_code, round):
        return [
            ["User message 1", "Assistant message 1"],
            ["User message 2", "Assistant message 2"],
        ]
    monkeypatch.setattr("app.service.conversation_service.get_conversation_history", mock_history)

def test_build_llm_request_message(mock_get_system_prompt_by_role_code, mock_get_conversation_history):
    user_input = "This is a test user input"
    role_code = 1

    messages = build_llm_request_message(user_input, role_code)

    expected_messages = [
        {"role": "system", "content": "Mocked System Prompt"},
        {"role": "user", "content": "User message 1"},
        {"role": "assistant", "content": "Assistant message 1"},
        {"role": "user", "content": "User message 2"},
        {"role": "assistant", "content": "Assistant message 2"},
        {"role": "user", "content": "This is a test user input"},
    ]

    assert messages == expected_messages


@pytest.fixture
def mock_get_message_repository(monkeypatch):
    mock_repo = MagicMock()

    monkeypatch.setattr("app.service.conversation_service.get_message_repository", lambda: mock_repo)

    return mock_repo


def test_get_conversation_history(mock_get_message_repository):
    mock_get_message_repository.get_latest_by.return_value = []

    history = get_conversation_history(role_code=1, round=1)
    assert len(history) == 0

    user_id1 = uuid.uuid4()

    user_message1 = Message(
        user_id=user_id1,
        role_code=1,
        content="Hello, this is a user message 1",
        message_type=MessageType.USER_MESSAGE,
    )
    assistant_message1 = Message(
        user_id=user_id1,
        role_code=1,
        content="Hello, this is a assistant message 1",
        message_type=MessageType.ASSISTANT_MESSAGE,
        parent_id=user_message1.id
    )
    user_message2 = Message(
        user_id=user_id1,
        role_code=1,
        content="Hello, this is a user message 2",
        message_type=MessageType.USER_MESSAGE,
        parent_id=assistant_message1.id
    )
    assistant_message2 = Message(
        user_id=user_id1,
        role_code=1,
        content="Hello, this is a assistant message 2",
        message_type=MessageType.ASSISTANT_MESSAGE,
        parent_id=user_message2.id
    )

    mock_get_message_repository.get_latest_by.return_value = [user_message1, assistant_message1, user_message2]

    history = get_conversation_history(role_code=1, round=1)
    assert len(history) == 1
    assert len(history[0]) == 2
    assert history[0][0] == "Hello, this is a user message 1"
    assert history[0][1] == "Hello, this is a assistant message 1"

    mock_get_message_repository.get_latest_by.return_value = [user_message1, assistant_message1, user_message2, assistant_message2]

    history = get_conversation_history(role_code=1, round=1)
    assert len(history) == 1
    assert len(history[0]) == 2
    assert history[0][0] == user_message2.content
    assert history[0][1] == assistant_message2.content
