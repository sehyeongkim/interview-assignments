import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.user.models import User
from app.user.services import UserService
from core.exceptions.user import DuplicatedUserEmail, UserNotFoundException


@pytest.mark.asyncio
async def test_insert_user():
    email = 'pms@gmail.com'
    user_info = {
        'name': '박명수',
        'gender': '남',
        'age': 30,
        'phone': '010-9999-0000',
        'email': email,
        'password': '1234'
    }
    result = await UserService().insert_user(user_info=user_info)
    assert type(result) == User
    assert result.email == email

@pytest.mark.asyncio
async def test_insert_user_duplicated(session: AsyncSession):
    user_info = {
        'name': '박명수',
        'gender': '남',
        'age': 30,
        'phone': '010-9999-0000',
        'email': 'pms@gmail.com',
        'password': '1234'
    }
    session.add(User(**user_info))
    await session.commit()
    with pytest.raises(DuplicatedUserEmail):
        await UserService().insert_user(user_info=user_info)

@pytest.mark.asyncio
async def test_get_user_by_email(session: AsyncSession):
    email = 'pms@gmail.com'
    user_info = {
        'name': '박명수',
        'email': email,
        'password': '1234'
    }
    session.add(User(**user_info))
    await session.commit()

    result = await UserService().get_user_by_email(user_email=email)
    assert type(result) == User
    assert result.email == email

@pytest.mark.asyncio
async def test_get_user_by_email_user_not_found():
    email = 'unregistered@gmail.com'
    with pytest.raises(UserNotFoundException):
        await UserService().get_user_by_email(user_email=email)

@pytest.mark.asyncio
async def test_get_users_list():
    pass

@pytest.mark.asyncio
async def test_get_user():
    pass

@pytest.mark.asyncio
async def test_get_user_does_not_exist():
    pass

@pytest.mark.asyncio
async def test_update_user():
    pass

@pytest.mark.asyncio
async def test_update_user_does_not_exist():
    pass

@pytest.mark.asyncio
async def test_delete_user():
    pass

@pytest.mark.asyncio
async def test_delete_user_does_not_exist():
    pass

@pytest.mark.asyncio
async def test_is_admin(session: AsyncSession):
    email = 'pms@gmail.com'
    user_info = {
        'name': '박명수',
        'email': email,
        'password': '1234',
        'is_admin': True
    }
    session.add(User(**user_info))
    await session.commit()
    user = await UserService().get_user_by_email(user_email=email)
    result = await UserService().is_admin(user_id=user.id_str)
    assert result is True

@pytest.mark.asyncio
async def test_is_admin_user_is_not_admin(session: AsyncSession):
    email = 'pms@gmail.com'
    user_info = {
        'name': '박명수',
        'email': email,
        'password': '1234',
        'is_admin': False
    }
    session.add(User(**user_info))
    await session.commit()
    user = await UserService().get_user_by_email(user_email=email)

    result = await UserService().is_admin(user_id=user.id_str)
    assert result is False
