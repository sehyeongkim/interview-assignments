from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.user.schemas import CreateUserRequestSchema, ModifyUserRequestSchema, GetUserResponseSchema, GetUsersListResponseSchema
from core.fastapi.dependencies.permission import PermissionDependency, IsAuthenticated, IsOwner, IsAdmin, IsOwnerOrAdmin

user_router = APIRouter()


@user_router.post(
    '',
    dependencies=[Depends(PermissionDependency([IsAdmin]))]
)
async def create_user(request: Request, create_user_request: CreateUserRequestSchema):
    pass


@user_router.get(
    '/{user_id}',
    response_model=GetUserResponseSchema,
    dependencies=[Depends(PermissionDependency([IsOwnerOrAdmin]))]
)
async def get_user(user_id: str):
    pass


@user_router.get(
    '',
    response_model=GetUsersListResponseSchema,
    dependencies=[Depends(PermissionDependency([IsAdmin]))]
)
async def get_users_list():
    pass


@user_router.put(
    '/{user_id}',
    dependencies=[Depends(PermissionDependency([IsOwnerOrAdmin]))]
)
async def modify_user(user_id: str, modify_user_request: ModifyUserRequestSchema):
    pass


@user_router.delete(
    '/{user_id}',
    dependencies=[Depends(PermissionDependency([IsOwnerOrAdmin]))]
)
async def delete_user(user_id: str):
    pass
