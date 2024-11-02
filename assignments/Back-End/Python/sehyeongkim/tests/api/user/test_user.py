import pytest

from httpx import AsyncClient
from sqlalchemy import select
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
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["superuser_token"]}'}
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
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/users", headers=headers, json=body)

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_user_invalid_request_required_field_not_exists(session: AsyncSession):
    body = {
        'email': 'pms@gmail.com',
        'password': '1234'
    }
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["superuser_token"]}'}
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
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["superuser_token"]}'}
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
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/users", headers=headers, json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_user_by_admin(session: AsyncSession):
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f"/api/v1/users/{data['user_id']}", headers=headers)

    result = response.json()
    assert response.status_code == 200
    assert 'id' in result
    assert 'name' in result
    assert 'gender' in result
    assert 'age' in result
    assert 'phone' in result
    assert 'email' in result
    assert 'is_admin' in result

@pytest.mark.asyncio
async def test_get_user_by_owner(session: AsyncSession):
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f"/api/v1/users/{data['user_id']}", headers=headers)

    result = response.json()
    assert response.status_code == 200
    assert 'id' in result
    assert 'name' in result
    assert 'gender' in result
    assert 'age' in result
    assert 'phone' in result
    assert 'email' in result
    assert 'is_admin' in result

@pytest.mark.asyncio
async def test_get_user_owner_forbidden(session: AsyncSession):
    email = 'pms@gmail.com'
    session.add(User(name='박명수', email=email, password='1234'))
    await session.commit()
    user = await session.execute(select(User).where(User.email == email))
    result = user.scalars().first()

    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f"/api/v1/users/{result.id_str}", headers=headers)

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_users_list(session: AsyncSession):
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f"/api/v1/users", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_get_users_list_forbidden(session: AsyncSession):
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f"/api/v1/users", headers=headers)

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_modify_user_by_admin(session: AsyncSession):
    new_name = 'new_name'
    body = {'name': new_name}
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/users/{data['user_id']}", headers=headers, json=body)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_modify_user_by_owner (session: AsyncSession):
    new_name = 'new_name'
    body = {'name': new_name}
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/users/{data['user_id']}", headers=headers, json=body)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_modify_user_invalid_request(session: AsyncSession):
    body = {'phone': '010-999-0000'}
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/users/{data['user_id']}", headers=headers, json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_modify_user_empty_request(session: AsyncSession):
    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/users/{data['user_id']}", headers=headers, json={})

    assert response.status_code == 400

@pytest.mark.asyncio
async def test_modify_user_forbidden(session: AsyncSession):
    email = 'pms@gmail.com'
    session.add(User(name='박명수', email=email, password='1234'))
    await session.commit()
    result = await session.execute(select(User).where(User.email==email))
    user = result.scalars().first()

    data = await create_users(session)
    headers = {'Authorization': f'Bearer {data["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/users/{user.id_str}", headers=headers, json={})

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_user():
    pass

@pytest.mark.asyncio
async def test_delete_user_not_found():
    pass
