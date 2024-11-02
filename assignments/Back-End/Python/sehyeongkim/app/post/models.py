import uuid
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.dialects.mysql import BINARY

from core.db.session import Base
from core.db.mixins import TimestampMixin


class Post(Base, TimestampMixin):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BINARY(16), nullable=False)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)

    @property
    def user_id_str(self):
        return str(uuid.UUID(bytes=self.user_id))
