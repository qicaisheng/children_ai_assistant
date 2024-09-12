import datetime
from enum import Enum
from typing import List, Optional
import uuid
from pydantic import BaseModel, Field
from core.role import get_current_role

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

def save_message(message: Message) -> Message:
    messages.append(dict(message))
    return message

def get_conversation_history(role_code: int, round: int) -> List[List[Optional[str]]]:
    filtered_messages = [msg for msg in messages[-(2*round+1):] if msg["role_code"] == role_code]
        
    conversation_history = []

    for message in filtered_messages:
        if message["message_type"] == MessageType.USER_MESSAGE:
            conversation_history.append([message["content"], None])
        elif message["message_type"] == MessageType.ASSISTANT_MESSAGE:
            if conversation_history and conversation_history[-1][1] is None:
                conversation_history[-1][1] = message["content"]

    if conversation_history and conversation_history[-1][1] is None:
        return conversation_history[-(round+1):-1]
    else:
        return conversation_history[-round:]
    
def get_current_role_messages(last_message_num: Optional[int] = None) -> List[Message]:
    current_role = get_current_role()
    
    filtered_messages = [Message(**msg) for msg in messages if msg["role_code"] == current_role.code]

    if last_message_num:
        return filtered_messages[-last_message_num:]
    else:
        return filtered_messages
    