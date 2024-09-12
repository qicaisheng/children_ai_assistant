import datetime
import uuid
from core.conversation_message import Message, MessageType
from repository.message import InMemoryMessageRepository, LatestMessagesFilter


def test_InMemoryMessageRepository_get_by_id():
    test_message = Message(
        user_id=uuid.uuid4(),
        role_code=1,
        content="Hello, this is a test message.",
        message_type=MessageType.USER_MESSAGE,
    )

    repository = InMemoryMessageRepository()
    saved_message = repository.save(test_message)

    assert type(saved_message) is Message
    assert saved_message.id is not None
    assert type(saved_message.id) is uuid.UUID
    assert saved_message.created_time is not None
    assert type(saved_message.created_time) is datetime.datetime
    assert saved_message.content == "Hello, this is a test message."
    assert saved_message.message_type == MessageType.USER_MESSAGE

def test_InMemoryMessageRepository_get_latest_by():    
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
        content="Hello, this is a assistant message 1",
        audio_id=["assistant_audio1", "assistant_audio2"],
        message_type=MessageType.ASSISTANT_MESSAGE,
        parent_id=user_message1.id
    )
    user_message2_role2 = Message(
        user_id=user_id,
        role_code=2,
        content="Hello, this is a user message 2",
        audio_id=["user_audio2"],
        message_type=MessageType.USER_MESSAGE,
        parent_id=assistant_message1.id
    )

    repository = InMemoryMessageRepository()

    repository.save(user_message1)
    repository.save(assistant_message1)
    repository.save(user_message2_role2)


    messages = repository.get_latest_by(LatestMessagesFilter(role_code=1, number=3))

    assert len(messages) == 2
    assert isinstance(messages[0], Message)

    messages = repository.get_latest_by(LatestMessagesFilter(role_code=1, number=1))

    assert len(messages) == 1
    assert messages[0].content == assistant_message1.content
    assert messages[0].audio_id == assistant_message1.audio_id
