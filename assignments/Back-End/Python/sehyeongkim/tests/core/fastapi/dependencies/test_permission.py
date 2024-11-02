import pytest
from fastapi import Request
from unittest.mock import AsyncMock, Mock

from core.exceptions.base import UnauthorizedException, ForbiddenException
from core.fastapi.dependencies.permission import PermissionDependency, IsAuthenticated, IsAdmin, IsOwnerOrAdmin, IsPostOwner


@pytest.mark.asyncio
async def test_permission_dependency_is_authenticated():
    dependency = PermissionDependency(permissions=[IsAuthenticated])
    request = AsyncMock(spec=Request)
    request.user = Mock(id=None)

    with pytest.raises(UnauthorizedException):
        await dependency(request=request)

@pytest.mark.asyncio
async def test_permission_dependency_is_admin():
    dependency = PermissionDependency(permissions=[IsAdmin])
    request = AsyncMock(spec=Request)
    request.user = Mock(id=None)

    with pytest.raises(ForbiddenException):
        await dependency(request=request)

@pytest.mark.asyncio
async def test_permission_dependency_is_owner_or_admin():
    dependency = PermissionDependency(permissions=[IsOwnerOrAdmin])
    request = AsyncMock(spec=Request)
    request.user = Mock(id=None)

    with pytest.raises(ForbiddenException):
        await dependency(request=request)


@pytest.mark.asyncio
async def test_permission_dependency_is_post_owner():
    dependency = PermissionDependency(permissions=[IsPostOwner])
    request = AsyncMock(spec=Request)
    request.user = Mock(id=None)

    with pytest.raises(ForbiddenException):
        await dependency(request=request)
