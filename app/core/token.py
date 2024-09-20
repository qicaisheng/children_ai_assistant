from typing import Optional

from app.core.user import User

tokens: dict = {}


def save(token: str, user: User):
    tokens[token] = user


def get_user_by_token(token: str) -> Optional[User]:
    return tokens.get(token)
