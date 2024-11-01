import pytest

from httpx import AsyncClient
from fastapi.exceptions import RequestValidationError

from app.server import app
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
async def test_signin():
    pass

@pytest.mark.asyncio
async def test_signin_invalid_request():
    pass
