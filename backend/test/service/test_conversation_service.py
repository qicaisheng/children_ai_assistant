import pytest
from unittest.mock import patch
from service.conversation_service import build_llm_request_message

@pytest.fixture
def mock_get_system_prompt_by_role_code(monkeypatch):
    def mock_prompt(role_code):
        return "Mocked System Prompt"
    monkeypatch.setattr("service.conversation_service.get_system_prompt_by_role_code", mock_prompt)

@pytest.fixture
def mock_get_conversation_history(monkeypatch):
    def mock_history(role_code, round):
        return [
            ["User message 1", "Assistant message 1"],
            ["User message 2", "Assistant message 2"],
        ]
    monkeypatch.setattr("service.conversation_service.get_conversation_history", mock_history)

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
