import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.post.models import Post
from app.post.services import PostService
from app.user.services import convert_uuid

@pytest.mark.asyncio
async def test_insert_post():
    pass

@pytest.mark.asyncio
async def test_get_posts_list(session: AsyncSession, create_users: dict):
    post = Post(title='제목', content='내용', user_id=convert_uuid(create_users['user_id']))
    session.add(post)
    await session.commit()
    await session.refresh(post)

    result = await PostService().get_posts()
    assert len(result) != 0

@pytest.mark.asyncio
async def test_get_post():
    pass

@pytest.mark.asyncio
async def test_update_post():
    pass

@pytest.mark.asyncio
async def test_update_post_does_not_exist():
    pass

@pytest.mark.asyncio
async def test_is_post_owner():
    pass

@pytest.mark.asyncio
async def test_is_post_owner_not_owner():
    pass
