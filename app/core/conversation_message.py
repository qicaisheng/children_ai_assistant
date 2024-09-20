import datetime
from enum import Enum
from typing import List, Optional
import uuid
from pydantic import BaseModel, Field
from app.core.role import get_current_role

messages = []

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


def get_current_role_messages(last_message_num: Optional[int] = None) -> List[Message]:
    current_role = get_current_role()
    
    filtered_messages = [Message(**msg) for msg in messages if msg["role_code"] == current_role.code]

    if last_message_num:
        return filtered_messages[-last_message_num:]
    else:
        return filtered_messages
    