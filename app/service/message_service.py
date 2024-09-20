from app.core.conversation_message import Message
from app.core.role import get_current_role
from app.core.user import get_default_user
from app.repository.message import MessageRepository, LatestMessagesFilter, get_message_repository


class MessageService:

    def __init__(self, repository: MessageRepository):
        self.repository = repository

    def save(self, message: Message) -> Message:
        return self.repository.save(message)

    def get_latest_by(self, messages_filter: LatestMessagesFilter) -> list[Message]:
        return self.repository.get_latest_by(messages_filter)

    def get_latest_current_user_and_role_messages(self, number: int) -> list[Message]:
        user = get_default_user()
        role = get_current_role()
        messages_filter = LatestMessagesFilter(user_id=user.id, role_code=role.code, number=number)
        return self.repository.get_latest_by(messages_filter)


def get_message_service() -> MessageService:
    return MessageService(get_message_repository())
