from pydantic import BaseModel


class User(BaseModel):
    name: str
    nickname: str
    gender: str = None
    age: int = None
    description: str = None

_default_user = {
    "name": "小朋友",
    "nickname": "小朋友",
    "age": 3,
}

def get_current_user() -> User:
    return User(**_default_user)