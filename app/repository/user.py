import datetime
import uuid
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, DateTime
from app.system.db import Base
from app.core.user import User


class UserInDB(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    device_sn = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    nickname = Column(String)
    gender = Column(String)
    age = Column(Integer)
    description = Column(Text)
    created_time = Column(DateTime(timezone=True), nullable=False,
                          default=lambda: datetime.datetime.now(datetime.timezone.utc))


class UserRepository:
    def __init__(self, session):
        self.session = session

    def save(self, user: User):
        user_in_db = UserInDB(
            id=str(user.id),
            device_sn=user.device_sn,
            name=user.name,
            nickname=user.nickname,
            gender=user.gender,
            age=user.age,
            description=user.description,
            created_time=user.created_time
        )
        self.session.add(user_in_db)
        self.session.commit()

    def get_by_device_sn(self, device_sn: str) -> Optional[User]:
        user_in_db = self.session.query(UserInDB).filter_by(device_sn=device_sn).first()
        if user_in_db:
            return User(
                id=user_in_db.id,
                device_sn=user_in_db.device_sn,
                name=user_in_db.name,
                nickname=user_in_db.nickname,
                gender=user_in_db.gender,
                age=user_in_db.age,
                description=user_in_db.description,
            )
        return None
