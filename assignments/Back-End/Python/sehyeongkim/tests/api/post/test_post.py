import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.server import app

@pytest.mark.asyncio
async def test_get_posts_list(create_users: dict):
    headers = {'Authorization': f'Bearer {create_users["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get("/api/v1/posts", headers=headers)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_posts_list_unauthorized(create_users: dict):
    headers = {'Authorization': 'Bearer '}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get("/api/v1/posts", headers=headers)

    assert response.status_code == 401

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
async def test_get_post():
    pass

@pytest.mark.asyncio
async def test_get_post_not_found():
    pass

@pytest.mark.asyncio
async def test_modify_post():
    pass

@pytest.mark.asyncio
async def test_modify_post_invalid_request():
    pass

@pytest.mark.asyncio
async def test_modify_post_not_found():
    pass
