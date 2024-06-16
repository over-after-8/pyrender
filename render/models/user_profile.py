from sqlalchemy import BigInteger, Column, String, Date, ForeignKey
from sqlalchemy.orm import mapped_column

from render.utils.base import basic_fields, Base


@basic_fields
class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = mapped_column(BigInteger, primary_key=True, nullable=False)
    name = Column(String(63), nullable=False)
    gender = Column(String(8), nullable=True)
    birth_date = Column(Date, nullable=True)
    avatar = Column(String(255), nullable=True)

    def __repr__(self):
        return f"{self.name}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_date": self.birth_date,
            "avatar": self.avatar
        }
