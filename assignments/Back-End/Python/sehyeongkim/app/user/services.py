import uuid
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, select, update, delete, insert

from app.user.models import User
from core.db.session import session
from core.db.transactional import Transactional
from core.exceptions.user import DuplicatedUserEmail, UserNotFoundException

class UserService:
    def __init__(self):
        pass

    @Transactional()
    async def insert_user(self, user_info: dict) -> User:
        user = User(**user_info)
        try:
            session.add(user)
            await session.flush()
        except IntegrityError:
            raise DuplicatedUserEmail
        return user

    async def get_user_by_email(self, user_email: str) -> User:
        stmt = select(User).where(User.email == user_email)
        result = await session.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException
        return user

    async def get_users(self):
        pass

    @Transactional()
    async def update_user(self):
        pass

    @Transactional()
    async def delete_user(self):
        pass

    async def is_admin(self, user_id: str) -> bool:
        stmt = select(User).where(User.id == uuid.UUID(user_id).bytes)
        result = await session.execute(stmt)
        user = result.scalars().first()
        if not user:
            return False

        return True if user.is_admin else False
