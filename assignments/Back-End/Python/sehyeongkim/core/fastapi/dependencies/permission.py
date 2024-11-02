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
        return request.user.id is not None


class IsAdmin(BasePermission):
    exception = ForbiddenException

    async def has_permission(self, request: Request) -> bool:
        return await UserService().is_admin(user_id=request.user.id)


class IsOwnerOrAdmin(BasePermission):
    exception = ForbiddenException

    async def has_permission(self, request: Request) -> bool:
        user_id = request.path_params.get('user_id', None)
        if user_id is None:
            return False

        is_admin = await UserService().is_admin(user_id=request.user.id)
        return True if request.user.id == user_id or is_admin else False


class IsPostOwner(BasePermission):
    exception = ForbiddenException

    async def has_permission(self, request: Request) -> bool:
        post_id = request.path_params.get('post_id', None)
        if post_id is None:
            return False
        return await PostService().is_post_owner(post_id=post_id, user_id=request.user.id)


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
