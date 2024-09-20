from app.core.conversation_message import Message
from app.repository.message import MessageRepository, LatestMessagesFilter, get_message_repository


class MessageService:

    def __init__(self, repository: MessageRepository):
        self.repository = repository

    def save(self, message: Message) -> Message:
        return self.repository.save(message)

    def get_latest_by(self, messages_filter: LatestMessagesFilter) -> list[Message]:
        return self.repository.get_latest_by(messages_filter)


def get_message_service() -> MessageService:
    return MessageService(get_message_repository())
