from typing import List

from sqlalchemy import Column, BigInteger, String, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from render.models.permission import Permission
from render.utils.base import Base, basic_fields

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id")),
    Column("permission_id", ForeignKey("permissions.id"))
)


@basic_fields
class Role(Base):
    __tablename__ = "roles"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(63), unique=True, nullable=False, index=True)

    permissions: Mapped[List[Permission]] = relationship(secondary=role_permissions)

    def __repr__(self):
        return f"{self.name}"

    def to_dict(self, session=None):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
