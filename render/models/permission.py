from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import mapped_column

from render.utils.base import Base, basic_fields


@basic_fields
class Permission(Base):
    __tablename__ = "permissions"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(63), unique=True, nullable=False, index=True)

    def __repr__(self):
        return f"{self.name}"

    def to_dict(self, session=None):
        return {
            "id": self.id,
            "name": self.name
        }
