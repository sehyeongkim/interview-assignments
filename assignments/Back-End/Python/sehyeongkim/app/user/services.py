import uuid
import datetime as dt
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, select, update, delete, insert

from app.user.models import User
from core.db.session import session
from core.db.transactional import Transactional
from core.exceptions.user import DuplicatedUserEmail, UserNotFoundException

def convert_uuid(id: str) -> bytes:
    return uuid.UUID(id).bytes

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

    async def get_user_by_id(self, user_id: str) -> User:
        try:
            stmt = select(User).where(User.id == convert_uuid(user_id))
            result = await session.execute(stmt)
        except ValueError:
            raise UserNotFoundException

        user = result.scalars().first()
        if not user:
            raise UserNotFoundException
        return user

    async def get_users(self) -> List[User]:
        stmt = select(User).where(User.deleted_at == None)
        result = await session.execute(stmt)
        return result.scalars().all()

    @Transactional()
    async def update_user(self, user_id: str, user_info: dict) -> None:
        stmt1 = select(User).where(User.id == convert_uuid(user_id))
        result = await session.execute(stmt1)
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException

        stmt = update(User).values(**user_info).where(User.id == convert_uuid(user_id))
        await session.execute(stmt)

    @Transactional()
    async def delete_user(self, user_id: str) -> None:
        get_user_stmt = select(User).where(User.id == convert_uuid(user_id))
        result = await session.execute(get_user_stmt)
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException

        stmt = update(User).values(deleted_at=dt.datetime.utcnow()).where(User.id == convert_uuid(user_id))
        await session.execute(stmt)

    async def is_admin(self, user_id: str) -> bool:
        stmt = select(User).where(User.id == convert_uuid(user_id))
        result = await session.execute(stmt)
        user = result.scalars().first()
        if not user:
            return False

        return True if user.is_admin else False
