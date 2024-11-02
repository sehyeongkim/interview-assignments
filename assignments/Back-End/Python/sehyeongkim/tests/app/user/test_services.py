import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.models import User
from app.user.services import UserService
from core.exceptions.user import DuplicatedUserEmail, UserNotFoundException

from tests.support import create_users, NOT_FOUND_UUID


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
async def test_get_users_list(session: AsyncSession):
    _ = await create_users(session)
    result = await UserService().get_users()
    assert len(result) == 2

@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    email = 'pms@gmail.com'
    user_info = {
        'name': '박명수',
        'email': email,
        'password': '1234'
    }
    session.add(User(**user_info))
    await session.commit()
    user = await session.execute(select(User).where(User.email == email))
    user_id = user.scalars().first().id_str

    result = await UserService().get_user_by_id(user_id=user_id)
    assert isinstance(result, User)

@pytest.mark.asyncio
async def test_get_user_by_id_does_not_exist():
    with pytest.raises(UserNotFoundException):
        await UserService().get_user_by_id(user_id='test')

@pytest.mark.asyncio
async def test_update_user(session: AsyncSession):
    email = 'pms@gmail.com'
    user_info = {
        'name': '박명수',
        'email': email,
        'password': '1234'
    }
    session.add(User(**user_info))
    await session.commit()
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    new_name = '활명수'
    await UserService().update_user(user_id=user.id_str, user_info={'name': new_name})

    stmt = select(User).where(User.id==user.id)
    result = await session.execute(stmt)
    updated_user = result.scalars().first()

    assert updated_user.name == new_name

@pytest.mark.asyncio
async def test_update_user_does_not_exist():
    with pytest.raises(UserNotFoundException):
        await UserService().update_user(user_id=NOT_FOUND_UUID, user_info={'name': 'new_name'})

@pytest.mark.asyncio
async def test_delete_user(session: AsyncSession):
    email = 'pms@gmail.com'
    user_info = {
        'name': '박명수',
        'email': email,
        'password': '1234',
    }
    session.add(User(**user_info))
    await session.commit()
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    await UserService().delete_user(user_id=user.id_str)
    result = await session.execute(select(User).where(User.id==user.id))
    deleted_user = result.scalars().first()

    assert deleted_user.deleted_at != None

@pytest.mark.asyncio
async def test_delete_user_does_not_exist():
    with pytest.raises(UserNotFoundException):
        await UserService().delete_user(user_id=NOT_FOUND_UUID)

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
