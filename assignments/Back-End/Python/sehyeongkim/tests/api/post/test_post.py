import pytest

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.server import app
from app.post.models import Post

@pytest.mark.asyncio
async def test_get_posts_list(init: dict):
    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get("/api/v1/posts", headers=headers)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_post(init: dict):
    body = {
        'title': '제목',
        'content': '내용'
    }
    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/posts", headers=headers, json=body)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_post_invalid_request(init: dict):
    body = {
        'title': '제목',
    }
    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/posts", headers=headers, json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_post(init: dict):
    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f"/api/v1/posts/{init['post_id']}", headers=headers)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_modify_post(session: AsyncSession, init: dict):
    new_content = '수정'
    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/posts/{init['post_id']}", headers=headers, json={'content': new_content})

    assert response.status_code == 200
    stmt = select(Post).where(Post.id==init['post_id'])
    result = await session.execute(stmt)
    updated_post = result.scalars().first()
    assert updated_post.content == new_content


@pytest.mark.asyncio
async def test_modify_post_invalid_request(init: dict):
    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/posts/{init['post_id']}", headers=headers, json={'title': 'not allowed'})

    assert response.status_code == 422
