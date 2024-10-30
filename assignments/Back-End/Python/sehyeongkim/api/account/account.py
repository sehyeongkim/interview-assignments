from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.account.schemas import SignUpRequestSchema, SignInRequestSchema, SignUpSignInResponseSchema

account_router = APIRouter()


@account_router.post(
    '/signup',
    response_model=SignUpSignInResponseSchema,
)
async def signup(request: Request, signup_request: SignUpRequestSchema):
    pass


@account_router.post(
    '/signin',
    response_model=SignUpSignInResponseSchema,
)
async def signin(request: Request, signin_request: SignInRequestSchema):
    pass
