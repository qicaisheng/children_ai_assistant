from pydantic import BaseModel


class User(BaseModel):
    name: str
    nickname: str
    gender: str = None
    age: int = None
    description: str = None