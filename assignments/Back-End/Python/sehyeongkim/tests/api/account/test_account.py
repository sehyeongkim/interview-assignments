import pytest
from httpx import AsyncClient
from passlib.context import CryptContext
from fastapi.exceptions import RequestValidationError

from app.server import app
from app.user.models import User
from app.user.services import UserService


@pytest.mark.asyncio
async def test_signup():
    email = 'pms@gmail.com'
    body = {
        'name': '박명수',
        'gender': '남',
        'age': 30,
        'phone': '010-9999-0000',
        'email': email,
        'password': '1234'
    }
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/api/v1/signup", json=body)

    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()
    user = await UserService().get_user_by_email(user_email=email)
    assert user.email == email

@pytest.mark.asyncio
async def test_signup_invalid_request_required_field_not_exists():
    body = {
        'gender': '남',
        'age': 30,
        'phone': '010-9999-0000',
    }
    exc = RequestValidationError
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/api/v1/signup', json=body)

    assert response.status_code == 422
    assert 'error_code' in response.json()
    assert 'message' in response.json()

@pytest.mark.asyncio
async def test_signup_invalid_request_phone_number_not_valid():
    body = {
        'name': '박명수',
        'gender': '남',
        'age': 30,
        'phone': '010-999-0000',
        'email': 'psmgmail.com',
        'password': '1234'
    }
    exc = RequestValidationError
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/api/v1/signup', json=body)

    assert response.status_code == 422
    assert 'error_code' in response.json()
    assert 'message' in response.json()

@pytest.mark.asyncio
async def test_signup_invalid_request_email_not_valid():
    body = {
        'name': '박명수',
        'gender': '남',
        'age': 30,
        'phone': '010-9999-0000',
        'email': 'psmgmail.com',
        'password': '1234'
    }
    exc = RequestValidationError
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/api/v1/signup', json=body)

    assert response.status_code == 422
    assert 'error_code' in response.json()
    assert 'message' in response.json()

@pytest.mark.asyncio
async def test_signin(session, crypto_context):
    email = 'pms@gmail.com'
    password = '1234'
    user_info = {
        'name': '박명수',
        'email': email,
        'password': crypto_context.hash(password)
    }
    session.add(User(**user_info))
    await session.commit()

    body = {'email': email, 'password': password}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/api/v1/signin', json=body)

    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()

@pytest.mark.asyncio
async def test_signin_invalid_request():
    body = {
        'email': 'pms@gmail.com',
    }
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/api/v1/signin', json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_signin_invalid_request_email_not_valid():
    body = {
        'email': 'pmsgmail.com',
        'password': '1234'
    }
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/api/v1/signin', json=body)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_signin_invalid_request_password_does_not_match(session, crypto_context):
    email = 'pms@gmail.com'
    user_info = {
        'name': '박명수',
        'email': email,
        'password': crypto_context.hash('1234')
    }
    session.add(User(**user_info))
    await session.commit()

    body = {'email': email, 'password': '12'}
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/api/v1/signin', json=body)

    assert response.status_code == 400
