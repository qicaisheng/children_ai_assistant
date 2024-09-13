import uuid
from pydantic import BaseModel, Field


class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    device_sn: str
    name: str
    nickname: str
    gender: str = None
    age: int = None
    description: str = None

_default_user = {
    "id": uuid.UUID(int=0x12345678123456781234567812345678),
    "device_sn": "48ca439bbfdc",
    "name": "benny",
    "nickname": "benny",
    "age": 3,
}

def get_current_user() -> User:
    return User(**_default_user)