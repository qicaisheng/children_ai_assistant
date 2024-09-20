import datetime
import uuid
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import ARRAY, Column, DateTime, Integer, String, desc
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.core.conversation_message import Message, MessageType
from app.system.db import get_postgresql_session

Base = declarative_base()


class MessageInDB(Base):
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    role_code = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    audio_id = Column(ARRAY(String), nullable=True, default=[])
    message_type = Column(String, nullable=False)
    parent_id = Column(UUID(as_uuid=True), nullable=True)
    created_time = Column(DateTime(timezone=True), nullable=False,
                          default=lambda: datetime.datetime.now(datetime.timezone.utc))


class LatestMessagesFilter(BaseModel):
    user_id: uuid.UUID
    role_code: int
    number: int


class MessageRepository:  # Interface
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def save(self, message: Message) -> Message:
        raise NotImplementedError()

    def get_by_id(self, id: str) -> Optional[Message]:
        raise NotImplementedError()

    def get_latest_by(self, messages_filter: LatestMessagesFilter) -> list[Message]:
        raise NotImplementedError()


class InMemoryMessageRepository(MessageRepository):
    def __init__(self):
        self.data: list[Message] = []

    def save(self, message: Message) -> Message:
        self.data.append(message)
        return message

    def get_by_id(self, id: str) -> Optional[Message]:
        for message in self.data:
            if message.id == id:
                return message
        return None

    def get_latest_by(self, messages_filter: LatestMessagesFilter) -> list[Message]:
        filtered_messages = [msg for msg in self.data if
                             msg.role_code == messages_filter.role_code and msg.user_id == messages_filter.user_id]

        return filtered_messages[-messages_filter.number:]


class PgMessageRepository(MessageRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, message: Message) -> Message:
        message_in_db = MessageInDB(
            id=message.id,
            user_id=message.user_id,
            role_code=message.role_code,
            content=message.content,
            audio_id=message.audio_id,
            message_type=message.message_type.value,  # Assuming MessageType is an Enum
            parent_id=message.parent_id,
            created_time=message.created_time,
        )
        self.session.add(message_in_db)
        self.session.commit()
        return message

    def get_by_id(self, id: str) -> Optional[Message]:
        message_in_db = self.session.query(MessageInDB).filter_by(id=id).first()
        if message_in_db:
            return Message(
                id=message_in_db.id,
                user_id=message_in_db.user_id,
                role_code=message_in_db.role_code,
                content=message_in_db.content,
                audio_id=message_in_db.audio_id,
                message_type=MessageType(message_in_db.message_type),  # Enum conversion
                parent_id=message_in_db.parent_id,
                created_time=message_in_db.created_time,
            )
        return None

    def get_latest_by(self, messages_filter: LatestMessagesFilter) -> list[Message]:
        query = (
            self.session.query(MessageInDB)
            .filter_by(user_id=messages_filter.user_id, role_code=messages_filter.role_code)
            .order_by(desc(MessageInDB.created_time))
            .limit(messages_filter.number)
        )
        messages_in_db = query.all()
        return [
            Message(
                id=message_in_db.id,
                user_id=message_in_db.user_id,
                role_code=message_in_db.role_code,
                content=message_in_db.content,
                audio_id=message_in_db.audio_id,
                message_type=MessageType(message_in_db.message_type),
                parent_id=message_in_db.parent_id,
                created_time=message_in_db.created_time,
            )
            for message_in_db in sorted(messages_in_db, key=lambda msg: msg.created_time)
        ]


def get_message_repository() -> MessageRepository:
    session = get_postgresql_session()
    return PgMessageRepository(session)
