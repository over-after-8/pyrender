import random
import string

from flask_login import UserMixin
from sqlalchemy import BigInteger, Column, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import mapped_column, relationship

from render.utils.base import Base, basic_fields
from render.utils.db import provide_session


def generate_random_string(length=7):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", BigInteger, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", BigInteger, ForeignKey("permissions.id"), primary_key=True),
)

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", BigInteger, ForeignKey("users.id"), primary_key=True),
    Column("role_id", BigInteger, ForeignKey("roles.id"), primary_key=True),
)

user_modules = Table(
    "user_modules",
    Base.metadata,
    Column("user_id", BigInteger, ForeignKey("users.id"), primary_key=True),
    Column("module_id", BigInteger, ForeignKey("modules.id"), primary_key=True),
)


@basic_fields
class Module(Base):
    __tablename__ = "modules"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(63), unique=True, nullable=False, index=True)
    class_name = Column(String(4095), nullable=False)

    def __repr__(self):
        return f"{self.name}"

    @provide_session
    def to_dict(self, session=None):
        return {
            "name": self.name,
            "class_name": self.class_name,
            "id": self.id,
        }


@basic_fields
class User(Base, UserMixin):
    __tablename__ = "users"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    user_name = Column(String(63), unique=True, nullable=False, index=True)
    password = Column(String(4095), nullable=False, index=False)
    salt = Column(String(7), nullable=False, index=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    roles = relationship("Role", secondary=user_roles, back_populates="inc_users")
    modules = relationship("Module", secondary=user_modules)

    @provide_session
    def to_dict(self, session=None):
        return {
            "user_name": self.user_name,
            "name": self.user_name,
            "is_active": self.is_active,
            "roles": [role.name for role in self.roles],
            "modules": [module.name for module in self.modules],
        }


class Role(Base):
    __tablename__ = "roles"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(63), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)

    inc_users = relationship("User", secondary=user_roles, back_populates="roles")

    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

    @provide_session
    def to_dict(self, session=None):
        return {
            "name": self.name,
            "description": self.description,
            "permissions": [perm.name for perm in self.permissions],
        }


class Permission(Base):
    __tablename__ = "permissions"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(63), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

    @provide_session
    def to_dict(self, session=None):
        return {
            "name": self.name,
            "description": self.description,
        }
