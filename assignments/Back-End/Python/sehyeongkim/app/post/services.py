from typing import List
from sqlalchemy import or_, select, update, delete, insert

from app.post.models import Post
from app.user.services import convert_uuid
from core.db.session import session
from core.db.transactional import Transactional


class PostService:
    def __init__(self):
        pass

    @Transactional()
    async def insert_post(self, user_id: str, post_info: dict) -> Post:
        data = {**post_info, **{'user_id': convert_uuid(user_id)}}
        post = Post(**data)
        session.add(post)
        await session.flush()
        await session.refresh(post)
        return post

    async def get_posts(self) -> List[Post]:
        stmt = select(Post).where(Post.deleted_at==None)
        result = await session.execute(stmt)
        return result.scalars().all()

    @Transactional()
    async def update_post(self):
        pass

    async def is_post_owner(self, post_id: int, user_id: str) -> bool:
        stmt = select(Post).where(Post.id == post_id, Post.user_id == user_id)
        result = await session.execute(stmt)
        post = result.scalars().first()
        return False if not post else True
