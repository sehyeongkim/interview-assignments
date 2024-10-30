import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_get_posts_list():
    pass

@pytest.mark.asyncio
async def test_create_post():
    pass

@pytest.mark.asyncio
async def test_create_post_invalid_request():
    pass

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
