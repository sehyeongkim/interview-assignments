import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.server import app
from app.user.models import User

from tests.support import create_users

@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    body = {
        'name': '박명수',
        'email': 'pms@gmail.com',
        'password': '1234'
    }
    token, _ = await create_users(session)
    headers = {'Authorization': f'Bearer {token}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/users", headers=headers, json=body)

    assert response.status_code == 200
    assert response.json()['result'] == 'success'

@pytest.mark.asyncio
async def test_create_user_forbidden(session: AsyncSession):
    body = {
        'name': '박명수',
        'email': 'pms@gmail.com',
        'password': '1234'
    }
    _, token = await create_users(session)
    headers = {'Authorization': f'Bearer {token}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/users", headers=headers, json=body)

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_user_invalid_request_required_field_not_exists(session: AsyncSession):
    body = {
        'email': 'pms@gmail.com',
        'password': '1234'
    }
    token, _ = await create_users(session)
    headers = {'Authorization': f'Bearer {token}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/users", headers=headers, json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_invalid_request_email_not_valid(session: AsyncSession):
    body = {
        'name': '박명수',
        'phone': '010-9999-0000',
        'email': 'pmsgmail.com',
        'password': '1234'
    }
    token, _ = await create_users(session)
    headers = {'Authorization': f'Bearer {token}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/users", headers=headers, json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_invalid_request_phone_not_valid(session: AsyncSession):
    email = 'pms@gmail.com'
    body = {
        'name': '박명수',
        'phone': '010-999-0000',
        'email': email,
        'password': '1234'
    }
    token, _ = await create_users(session)
    headers = {'Authorization': f'Bearer {token}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/users", headers=headers, json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_user():
    pass

@pytest.mark.asyncio
async def test_get_user_not_found():
    pass

@pytest.mark.asyncio
async def test_get_users_list():
    pass

@pytest.mark.asyncio
async def test_modify_user():
    pass

@pytest.mark.asyncio
async def test_modify_user_invalid_request():
    pass

@pytest.mark.asyncio
async def test_modify_user_not_found():
    pass

@pytest.mark.asyncio
async def test_delete_user():
    pass

@pytest.mark.asyncio
async def test_delete_user_not_found():
    pass
