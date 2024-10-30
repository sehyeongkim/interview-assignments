from abc import ABC, abstractmethod
from typing import List, Type

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase

from app.user.services import UserService
from app.post.services import PostService
from core.exceptions.base import CustomException, ForbiddenException, UnauthorizedException


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        pass

class IsOwner(BasePermission):
    exception = ForbiddenException

    async def has_permission(self, request: Request) -> bool:
        pass


class IsAdmin(BasePermission):
    exception = ForbiddenException

    async def has_permission(self, request: Request) -> bool:
        pass


class IsOwnerOrAdmin(BasePermission):
    exception = ForbiddenException

    async def has_permission(self, request: Request) -> bool:
        pass


class IsPostOwner(BasePermission):
    exception = ForbiddenException

    async def has_permission(self, request: Request) -> bool:
        pass


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List[Type[BasePermission]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        for permission in self.permissions:
            cls = permission()
            if not await cls.has_permission(request=request):
                raise cls.exception
