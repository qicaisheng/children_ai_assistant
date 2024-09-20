import uuid
from repository.fixture_db import db_session
from app.core.user import User
from app.repository.user import UserRepository


def test_user_repository_save_and_get(db_session):
    repository = UserRepository(db_session)

    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        device_sn="SN12345",
        name="John Doe",
        nickname="Johnny",
        gender="male",
        age=30,
        description="A test user",
    )

    repository.save(user)

    retrieved_user = repository.get_by_device_sn("SN12345")

    assert retrieved_user is not None
    assert retrieved_user.id == user_id
    assert retrieved_user.name == "John Doe"
    assert retrieved_user.device_sn == "SN12345"
    assert retrieved_user.nickname == "Johnny"
    assert retrieved_user.gender == "male"
    assert retrieved_user.age == 30
    assert retrieved_user.description == "A test user"
