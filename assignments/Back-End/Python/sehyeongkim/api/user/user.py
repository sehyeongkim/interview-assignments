from passlib.context import CryptContext

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.user.services import UserService
from app.user.schemas import CreateUserRequestSchema, ModifyUserRequestSchema, GetUserResponseSchema, GetUsersListResponseSchema
from core.fastapi.dependencies.permission import PermissionDependency, IsAdmin, IsOwnerOrAdmin

user_router = APIRouter()


@user_router.post(
    '',
    dependencies=[Depends(PermissionDependency([IsAdmin]))]
)
async def create_user(request: Request, create_user_request: CreateUserRequestSchema):
    user_info = dict(create_user_request)
    user_info['password'] = CryptContext(schemes=['bcrypt']).hash(create_user_request.password)
    _ = await UserService().insert_user(user_info=user_info)
    return JSONResponse(content={'result': 'success'}, status_code=200)


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
