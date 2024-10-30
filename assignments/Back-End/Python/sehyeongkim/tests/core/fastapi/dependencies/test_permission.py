import pytest
from fastapi import Request
from unittest.mock import AsyncMock, Mock

from core.fastapi.dependencies.permission import PermissionDependency, IsAuthenticated, IsOwner, IsAdmin, IsOwnerOrAdmin, IsPostOwner


@pytest.mark.asyncio
async def test_permission_dependency_is_authenticated():
    pass

@pytest.mark.asyncio
async def test_permission_dependency_is_owner():
    pass

@pytest.mark.asyncio
async def test_permission_dependency_is_owner_not_owner():
    pass

@pytest.mark.asyncio
async def test_permission_dependency_is_admin():
    pass

@pytest.mark.asyncio
async def test_permission_dependency_is_admin_not_admin():
    pass

@pytest.mark.asyncio
async def test_permission_dependency_is_owner_or_admin():
    pass

@pytest.mark.asyncio
async def test_permission_dependency_is_owner_or_admin_neither():
    pass

@pytest.mark.asyncio
async def test_permission_dependency_is_post_owner():
    pass

@pytest.mark.asyncio
async def test_permission_dependency_is_post_owner_not_owner():
    pass
