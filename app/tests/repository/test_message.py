import datetime
import uuid
import pytest
from app.core.conversation_message import Message, MessageType
from app.repository.message import InMemoryMessageRepository, LatestMessagesFilter, PgMessageRepository
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.repository.message import MessageInDB, Base
from testcontainers.postgres import PostgresContainer
from alembic import command
from alembic.config import Config

@pytest.fixture(scope="module")
def db_session():
    with PostgresContainer("postgres:latest", driver="psycopg") as postgres:
        engine = create_engine(postgres.get_connection_url())

        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option('script_location', "../../alembic")
        alembic_cfg.set_main_option('sqlalchemy.url', postgres.get_connection_url())
        command.upgrade(alembic_cfg, "head")

        Session = sessionmaker(bind=engine)
        session = Session()
        yield session

        session.close()

# 公共测试逻辑，适用于不同的仓库类型
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
    repository.save(user_message1)
    repository.save(assistant_message1)

    messages = repository.get_latest_by(LatestMessagesFilter(role_code=1, number=2))

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
