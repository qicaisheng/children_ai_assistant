import uuid

from app.core.token import save, get_user_by_token
from app.core.user import User


def test_get_user_by_token():
    _default_user = {
        "id": uuid.UUID(int=0x12345678123456781234567812345678),
        "device_sn": "48ca439bbfdc",
        "name": "benny",
        "nickname": "benny",
        "age": 3,
    }

    save("123", User(**_default_user))

    user = get_user_by_token("123")
    assert user.id == _default_user.get("id")

    user = get_user_by_token("not_existed_token")
    assert user is None
