import random
import string

from flask_login import UserMixin
from sqlalchemy import BigInteger, Column, String, Boolean
from sqlalchemy.orm import mapped_column

from render.utils.base import Base, basic_fields
from render.utils.db import provide_session


def generate_random_string(length=7):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


@basic_fields
class User(Base, UserMixin):
    __tablename__ = "admin_users"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    user_name = Column(String(63), unique=True, nullable=False, index=True)
    password = Column(String(4095), nullable=False, index=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    @provide_session
    def to_dict(self, session=None):
        return {
            "user_name": self.user_name,
            "name": self.user_name,
            "is_active": self.is_active,
        }
