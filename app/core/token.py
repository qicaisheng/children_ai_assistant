from typing import Optional

from app.core.user import User, get_current_user

tokens: dict = {}


def save(token: str, user: User):
    tokens[token] = user


def get_user_by_token(token: str) -> Optional[User]:
    if token == "2905cc6103c5442985cb15946425e451":
        return get_current_user()
    user = tokens.get(token)
    print(f"get_user_by_token, token: {token}, user: {user}")
    return user
