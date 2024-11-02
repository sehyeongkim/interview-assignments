import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.post.models import Post
from app.post.services import PostService
from app.user.services import convert_uuid
from core.exceptions.post import PostNotFoundException


@pytest.mark.asyncio
async def test_insert_post(create_users: dict):
    data = {'title': '제목', 'content': '내용'}
    result = await PostService().insert_post(create_users['user_id'], data)
    assert isinstance(result, Post)

@pytest.mark.asyncio
async def test_get_posts_list(session: AsyncSession, create_users: dict):
    post = Post(title='제목', content='내용', user_id=convert_uuid(create_users['user_id']))
    session.add(post)
    await session.commit()
    await session.refresh(post)

    result = await PostService().get_posts()
    assert len(result) != 0

@pytest.mark.asyncio
async def test_get_post_by_id(session: AsyncSession, create_users: dict):
    post = Post(title='제목', content='내용', user_id=convert_uuid(create_users['user_id']))
    session.add(post)
    await session.commit()
    await session.refresh(post)

    result = await PostService().get_post_by_id(post_id=post.id)
    assert isinstance(result, Post)

@pytest.mark.asyncio
async def test_get_post_by_id_post_does_not_exist():
    with pytest.raises(PostNotFoundException):
        await PostService().get_post_by_id(post_id=1)

@pytest.mark.asyncio
async def test_update_post(session: AsyncSession, create_users: dict):
    post = Post(title='제목', content='내용', user_id=convert_uuid(create_users['user_id']))
    session.add(post)
    await session.commit()
    await session.refresh(post)

    new_content = '수정'
    await PostService().update_post(post_id=post.id, post_info={'content': new_content})

@pytest.mark.asyncio
async def test_update_post_does_not_exist():
    with pytest.raises(PostNotFoundException):
        await PostService().update_post(post_id=1, post_info={})

@pytest.mark.asyncio
async def test_is_post_owner(session: AsyncSession, create_users: dict):
    post = Post(title='제목', content='내용', user_id=convert_uuid(create_users['user_id']))
    session.add(post)
    await session.commit()
    await session.refresh(post)

    result = await PostService().is_post_owner(post_id=post.id, user_id=create_users['user_id'])
    assert result == True

@pytest.mark.asyncio
async def test_is_post_owner_not_owner(session: AsyncSession, create_users: dict):
    post = Post(title='제목', content='내용', user_id=convert_uuid(create_users['superuser_id']))
    session.add(post)
    await session.commit()
    await session.refresh(post)

    result = await PostService().is_post_owner(post_id=post.id, user_id=create_users['user_id'])
    assert result == False
