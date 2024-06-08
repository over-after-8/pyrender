from sqlalchemy import Integer, Column, String, Table, ForeignKey

from render.utils.base import basic_fields, Base

user_modules = Table(
    "user_modules",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("module_id", ForeignKey("modules.id"))
)


@basic_fields
class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(63), unique=True, nullable=False, index=True)
    class_name = Column(String(63), nullable=False)

    def __repr__(self):
        return f"{self.name}"

    def to_dict(self, session=None):
        return {
            "id": self.id,
            "name": self.name,
            "class_name": self.class_name
        }
