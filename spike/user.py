from pydantic import BaseModel


class User(BaseModel):
    name: str
    nickname: str
    gender: str
    age: int
    description: str