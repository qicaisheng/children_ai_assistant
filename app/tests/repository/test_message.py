import datetime
import uuid
from app.core.conversation_message import Message, MessageType
from app.repository.message import InMemoryMessageRepository, LatestMessagesFilter, PgMessageRepository
from repository.fixture_db import db_session


def common_test_save_message(repository):
    test_message = Message(
        user_id=uuid.uuid4(),
        role_code=1,
        content="Hello, this is a test message.",
        message_type=MessageType.USER_MESSAGE,
    )
    saved_message = repository.save(test_message)

    assert type(saved_message) is Message
    assert saved_message.id is not None
    assert type(saved_message.id) is uuid.UUID
    assert saved_message.created_time is not None
    assert type(saved_message.created_time) is datetime.datetime
    assert saved_message.content == "Hello, this is a test message."
    assert saved_message.message_type == MessageType.USER_MESSAGE

def common_test_get_latest_by(repository):
    user_id = uuid.uuid4()
    user_message1 = Message(
        user_id=user_id,
        role_code=1,
        content="Hello, this is a user message 1",
        audio_id=["user_audio1"],
        message_type=MessageType.USER_MESSAGE,
    )
    assistant_message1 = Message(
        user_id=user_id,
        role_code=1,
        content="Hello, this is an assistant message 1",
        audio_id=["assistant_audio1", "assistant_audio2"],
        message_type=MessageType.ASSISTANT_MESSAGE,
        parent_id=user_message1.id
    )
    user2_message1 = Message(
        user_id=uuid.uuid4(),
        role_code=1,
        content="Hello, this is a user2 message 1",
        audio_id=["user2_audio1"],
        message_type=MessageType.USER_MESSAGE,
    )
    repository.save(user_message1)
    repository.save(assistant_message1)
    repository.save(user2_message1)

    messages = repository.get_latest_by(LatestMessagesFilter(user_id=user_id, role_code=1, number=2))

    assert len(messages) == 2
    assert messages[0].content == user_message1.content
    assert messages[0].audio_id == user_message1.audio_id

# 测试 InMemoryMessageRepository
def test_InMemoryMessageRepository_save_message():
    repository = InMemoryMessageRepository()
    common_test_save_message(repository)

def test_InMemoryMessageRepository_get_latest_by():
    repository = InMemoryMessageRepository()
    common_test_get_latest_by(repository)

# 测试 PgMessageRepository（使用 SQLite 测试数据库）
def test_PgMessageRepository_save_message(db_session):
    repository = PgMessageRepository(db_session)
    common_test_save_message(repository)

def test_PgMessageRepository_get_latest_by(db_session):
    repository = PgMessageRepository(db_session)
    common_test_get_latest_by(repository)
