import dataclasses
import hashlib
import random
import string
from typing import List

from flask_login import UserMixin
from sqlalchemy import BigInteger, Column, String, TIMESTAMP, func, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, mapped_column, Mapped

from render.models.module import user_modules, Module
from render.models.role import Role
from render.utils.base import Base, basic_fields
from render.utils.db import provide_session


def generate_random_string(length=7):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class MD5:
    @staticmethod
    def hash_string(nake_string, salt_key):
        salted_string = nake_string + salt_key
        return hashlib.md5(salted_string.encode()).hexdigest()

    @staticmethod
    def validate_string(naked_string, salt_key, hashed_string):
        return hashed_string == MD5.hash_string(naked_string, salt_key)


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("role_id", ForeignKey("roles.id"))
)


@dataclasses.dataclass
@basic_fields
class User(Base, UserMixin):
    __tablename__ = "users"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    user_name = Column(String(63), unique=True, nullable=False, index=True)
    password = Column(String(4095), nullable=False, index=False)
    salt = Column(String(7), nullable=False, index=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    full_name = Column(String(63), nullable=True, index=True)

    roles: Mapped[List[Role]] = relationship(secondary=user_roles)
    modules: Mapped[List[Module]] = relationship(secondary=user_modules)

    def __repr__(self):
        return self.user_name

    @staticmethod
    @provide_session
    def get(user_id, session=None):
        return session.query(User).filter(User.id == user_id).one_or_none()

    def validate_password(self, password):
        return MD5.validate_string(password, self.salt, self.password)

    @staticmethod
    @provide_session
    def get_by_user_name_password(user_name, password, session=None):
        user = session.query(User).filter(User.user_name == user_name).one_or_none()
        return user and user.validate_password(password) and user or None

    @staticmethod
    @provide_session
    def add(user_name, password, created_by, session=None):
        salt = generate_random_string()
        password = MD5.hash_string(password, salt)
        user = User()
        user.user_name = user_name
        user.password = password
        user.salt = salt
        user.full_name = user_name.split("@")[0]
        user.is_active = True
        user.created_by = created_by

        return session.add(user)

    def get_id(self):
        return self.id

    @staticmethod
    @provide_session
    def update_password(user_id, password, session=None):
        user = session.query(User).filter(User.id == user_id).one_or_none()
        if user:
            salt = generate_random_string()
            password = MD5.hash_string(password, salt)
            user.password = password
            user.salt = salt
            return True
        return False
