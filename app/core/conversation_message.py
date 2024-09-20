import datetime
import uuid
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class MessageType(Enum):
    USER_MESSAGE = "USER_MESSAGE"
    ASSISTANT_MESSAGE = "ASSISTANT_MESSAGE"


class Message(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    role_code: int
    content: str
    audio_id: list[str] = []
    message_type: MessageType
    parent_id: Optional[uuid.UUID] = None
    created_time: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

