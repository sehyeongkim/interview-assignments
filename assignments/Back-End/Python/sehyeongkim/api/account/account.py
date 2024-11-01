from passlib.context import CryptContext

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.account.schemas import SignUpRequestSchema, SignInRequestSchema, SignUpSignInResponseSchema
from app.user.services import UserService
from core.utils.token_helper import TokenHelper
from core.exceptions.user import PasswordDoesNotMatchException

account_router = APIRouter()


@account_router.post(
    '/signup',
    response_model=SignUpSignInResponseSchema,
)
async def signup(request: Request, signup_request: SignUpRequestSchema):
    user_info = dict(signup_request)
    user_info['password'] = CryptContext(schemes=['bcrypt']).hash(signup_request.password)
    user = await UserService().insert_user(user_info)
    result = {'access_token': TokenHelper.encode({'user_id': user.id_str}),
              'refresh_token': TokenHelper.encode({'sub': 'refresh'})}
    return JSONResponse(content=result, status_code=200)


@account_router.post(
    '/signin',
    response_model=SignUpSignInResponseSchema,
)
async def signin(request: Request, signin_request: SignInRequestSchema):
    user_info = dict(signin_request)
    user = await UserService().get_user_by_email(user_info['email'])
    verified = CryptContext(schemes=['bcrypt']).verify(user_info['password'], user.password)
    if not verified:
        raise PasswordDoesNotMatchException
    result = {'access_token': TokenHelper.encode({'user_id': user.id_str}),
              'refresh_token': TokenHelper.encode({'sub': 'refresh'})}
    return JSONResponse(content=result, status_code=200)
