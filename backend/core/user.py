from pydantic import BaseModel


class User(BaseModel):
    name: str
    nickname: str
    gender: str = None
    age: int = None
    description: str = None

_default_user = {
    "name": "benny",
    "nickname": "benny",
    "age": 3,
}

def get_current_user() -> User:
    return User(**_default_user)