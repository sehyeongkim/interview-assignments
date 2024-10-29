from sqlalchemy import Column, String, Integer, Text

from core.db.session import Base
from core.db.mixins import TimestampMixin


class Post(Base, TimestampMixin):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20), nullable=False)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
