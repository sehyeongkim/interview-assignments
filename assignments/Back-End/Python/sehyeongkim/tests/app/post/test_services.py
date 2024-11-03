import pytest

from app.post.models import Post
from app.post.services import PostService

from core.exceptions.post import PostNotFoundException


@pytest.mark.asyncio
async def test_insert_post(init: dict):
    data = {'title': '제목', 'content': '내용'}
    result = await PostService().insert_post(init['user_id'], data)
    assert isinstance(result, Post)

@pytest.mark.asyncio
async def test_get_posts_list():
    result = await PostService().get_posts()
    assert len(result) != 0

@pytest.mark.asyncio
async def test_get_post_by_id(init: dict):
    result = await PostService().get_post_by_id(post_id=init['post_id'])
    assert isinstance(result, Post)

@pytest.mark.asyncio
async def test_get_post_by_id_post_does_not_exist():
    with pytest.raises(PostNotFoundException):
        await PostService().get_post_by_id(post_id=1)

@pytest.mark.asyncio
async def test_update_post(init: dict):
    new_content = '수정'
    await PostService().update_post(post_id=init['post_id'], post_info={'content': new_content})

@pytest.mark.asyncio
async def test_update_post_does_not_exist():
    with pytest.raises(PostNotFoundException):
        await PostService().update_post(post_id=1, post_info={})

@pytest.mark.asyncio
async def test_is_post_owner(init: dict):
    result = await PostService().is_post_owner(post_id=init['post_id'], user_id=init['user_id'])
    assert result == True

@pytest.mark.asyncio
async def test_is_post_owner_not_owner(init: dict):
    result = await PostService().is_post_owner(post_id=init['post_id'], user_id=init['superuser_id'])
    assert result == False
