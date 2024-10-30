import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_user():
    pass

@pytest.mark.asyncio
async def test_create_invalid_request():
    pass

@pytest.mark.asyncio
async def test_create_user_duplicated_email():
    pass

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
