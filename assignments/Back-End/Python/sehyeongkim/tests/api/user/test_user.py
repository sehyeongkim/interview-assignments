import pytest

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.server import app
from app.user.models import User


@pytest.mark.asyncio
async def test_create_user(init: dict):
    body = {
        'name': '박명수',
        'email': 'pms@gmail.com',
        'password': '1234'
    }
    headers = {'Authorization': f'Bearer {init["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/users", headers=headers, json=body)

    assert response.status_code == 200
    assert response.json()['result'] == 'success'

@pytest.mark.asyncio
async def test_create_user_forbidden(init: dict):
    body = {
        'name': '박명수',
        'email': 'pms@gmail.com',
        'password': '1234'
    }
    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/users", headers=headers, json=body)

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_user_invalid_request_required_field_not_exists(init: dict):
    body = {
        'email': 'pms@gmail.com',
        'password': '1234'
    }
    headers = {'Authorization': f'Bearer {init["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/users", headers=headers, json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_invalid_request_email_not_valid(init: dict):
    body = {
        'name': '박명수',
        'phone': '010-9999-0000',
        'email': 'pmsgmail.com',
        'password': '1234'
    }
    headers = {'Authorization': f'Bearer {init["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/users", headers=headers, json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_invalid_request_phone_not_valid(init: dict):
    email = 'pms@gmail.com'
    body = {
        'name': '박명수',
        'phone': '010-999-0000',
        'email': email,
        'password': '1234'
    }
    headers = {'Authorization': f'Bearer {init["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/users", headers=headers, json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_user_by_admin(init: dict):
    headers = {'Authorization': f'Bearer {init["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f"/api/v1/users/{init['user_id']}", headers=headers)

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
async def test_get_user_by_owner(init: dict):
    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f"/api/v1/users/{init['user_id']}", headers=headers)

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
async def test_get_user_owner_forbidden(session: AsyncSession, init: dict):
    email = 'pms@gmail.com'
    session.add(User(name='박명수', email=email, password='1234'))
    await session.commit()
    user = await session.execute(select(User).where(User.email == email))
    result = user.scalars().first()

    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f"/api/v1/users/{result.id_str}", headers=headers)

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_users_list(init: dict):
    headers = {'Authorization': f'Bearer {init["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f"/api/v1/users", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_get_users_list_forbidden(init: dict):
    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f"/api/v1/users", headers=headers)

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_modify_user_by_admin(init: dict):
    new_name = 'new_name'
    body = {'name': new_name}
    headers = {'Authorization': f'Bearer {init["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/users/{init['user_id']}", headers=headers, json=body)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_modify_user_by_owner (init: dict):
    new_name = 'new_name'
    body = {'name': new_name}
    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/users/{init['user_id']}", headers=headers, json=body)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_modify_user_invalid_request(init: dict):
    body = {'phone': '010-999-0000'}
    headers = {'Authorization': f'Bearer {init["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/users/{init['user_id']}", headers=headers, json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_modify_user_empty_request(init: dict):
    headers = {'Authorization': f'Bearer {init["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/users/{init['user_id']}", headers=headers, json={})

    assert response.status_code == 400

@pytest.mark.asyncio
async def test_modify_user_forbidden(session: AsyncSession, init: dict):
    email = 'pms@gmail.com'
    session.add(User(name='박명수', email=email, password='1234'))
    await session.commit()
    result = await session.execute(select(User).where(User.email==email))
    user = result.scalars().first()

    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.put(f"/api/v1/users/{user.id_str}", headers=headers, json={})

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_user_by_owner(session: AsyncSession, init: dict):
    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.delete(f"/api/v1/users/{init['user_id']}", headers=headers)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_user_by_admin(session: AsyncSession, init: dict):
    headers = {'Authorization': f'Bearer {init["superuser_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.delete(f"/api/v1/users/{init['user_id']}", headers=headers)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_forbidden(session: AsyncSession, init: dict):
    email = 'pms@gmail.com'
    session.add(User(name='박명수', email=email, password='1234'))
    await session.commit()
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    headers = {'Authorization': f'Bearer {init["user_token"]}'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.delete(f"/api/v1/users/{user.id_str}", headers=headers)

    assert response.status_code == 403
