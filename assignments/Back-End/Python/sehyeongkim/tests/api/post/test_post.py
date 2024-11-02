import uuid
import pytest

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.server import app
from app.post.models import Post

@pytest.mark.asyncio
async def test_get_posts_list(create_users: dict):
    headers = {'Authorization': f'Bearer {create_users["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get("/api/v1/posts", headers=headers)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_post(create_users: dict):
    body = {
        'title': '제목',
        'content': '내용'
    }
    headers = {'Authorization': f'Bearer {create_users["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/posts", headers=headers, json=body)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_post_invalid_request(create_users: dict):
    body = {
        'title': '제목',
    }
    headers = {'Authorization': f'Bearer {create_users["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/posts", headers=headers, json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_post(session: AsyncSession, create_users: dict):
    post = Post(title='제목', content='내용', user_id=uuid.UUID(create_users['superuser_id']).bytes)
    session.add(post)
    await session.commit()
    await session.refresh(post)

    headers = {'Authorization': f'Bearer {create_users["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f"/api/v1/posts/{post.id}", headers=headers)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_modify_post(session: AsyncSession, create_users: dict):
    post = Post(title='제목', content='내용', user_id=uuid.UUID(create_users['user_id']).bytes)
    session.add(post)
    await session.commit()
    await session.refresh(post)

    new_content = '수정'
    headers = {'Authorization': f'Bearer {create_users["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/posts/{post.id}", headers=headers, json={'content': new_content})

    assert response.status_code == 200
    stmt = select(Post).where(Post.id==post.id)
    result = await session.execute(stmt)
    updated_post = result.scalars().first()
    assert updated_post.content == new_content


@pytest.mark.asyncio
async def test_modify_post_invalid_request(session: AsyncSession, create_users: dict):
    post = Post(title='제목', content='내용', user_id=uuid.UUID(create_users['user_id']).bytes)
    session.add(post)
    await session.commit()
    await session.refresh(post)

    headers = {'Authorization': f'Bearer {create_users["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/posts/{post.id}", headers=headers, json={'title': 'not allowed'})

    assert response.status_code == 422
