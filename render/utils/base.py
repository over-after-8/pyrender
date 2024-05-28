from sqlalchemy import Column, TIMESTAMP, func, ForeignKey, BigInteger, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def basic_fields(cls):
    cls.created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    cls.updated_at = Column(TIMESTAMP, default=func.now(), nullable=False)

    return cls


def owner_field(back_populates):
    def wrapper(cls):
        from render.models.user import User
        cls.owner_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
        cls.owner = relationship("User", back_populates=back_populates)
        setattr(User, back_populates, relationship(cls.__name__, back_populates="owner"))
        return cls

    return wrapper


def permission_field(default=7):
    def wrapper(cls):
        cls.permission = Column(Integer, nullable=False, default=default)
        return cls

    return wrapper
