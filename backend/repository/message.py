from typing import Optional

from pydantic import BaseModel
from core.conversation_message import Message, MessageType


class LatestMessagesFilter(BaseModel):
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
        filtered_messages = [msg for msg in self.data if msg.role_code == messages_filter.role_code]

        return filtered_messages[-messages_filter.number:]
