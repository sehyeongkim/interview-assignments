import uuid
from sqlalchemy import Column, Boolean, String, Integer, Text
from sqlalchemy.dialects.mysql import BINARY

from core.db.session import Base
from core.db.mixins import TimestampMixin


def generate_uuid():
    return uuid.uuid4().bytes


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(BINARY(16), primary_key=True, default=generate_uuid)
    name = Column(String(10), nullable=False)
    gender = Column(String(5))
    age = Column(Integer)
    phone = Column(String(20))
    email = Column(String(50), nullable=False)
    password = Column(Text, nullable=False)
    is_admin = Column(Boolean, default=False)
