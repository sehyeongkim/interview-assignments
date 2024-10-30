import pytest

from app.user.services import UserService


@pytest.mark.asyncio
async def test_insert_user():
    pass

@pytest.mark.asyncio
async def test_insert_user_duplicated():
    pass

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
async def test_is_admin():
    pass

@pytest.mark.asyncio
async def test_is_admin_user_is_not_admin():
    pass
