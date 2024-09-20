import datetime
import uuid
from pydantic import BaseModel, Field
from contextvars import ContextVar


class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    device_sn: str
    name: str
    nickname: str
    gender: str = None
    age: int = None
    description: str = None
    created_time: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))


_default_user = {
    "id": uuid.UUID(int=0x12345678123456781234567812345678),
    "device_sn": "48ca439bbfdc",
    "name": "benny",
    "nickname": "benny",
    "age": 3,
}

def get_default_user() -> User:
    return User(**_default_user)


def get_current_user_from_context() -> User:
    return user_context.get()


def set_current_user(user: User):
    print(f"set_current_user, user:{user}")
    user_context.set(user)


user_context: ContextVar[User] = ContextVar("user_context")
