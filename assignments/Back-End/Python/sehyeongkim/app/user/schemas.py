from typing import Optional, List
from pydantic import BaseModel, Field


class CreateUserRequestSchema(BaseModel):
    name: str = Field(..., description='사용자 이름')
    gender: str = Field(None, description='성별')
    age: int = Field(None, description='나이')
    phone: str = Field(None, pattern=r'^010-\d{4}-\d{4}$', description='핸드폰 번호')
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', description='이메일(아이디)')
    password: str = Field(..., description='비밀번호')
    is_admin: Optional[bool] = Field(False, description='관리자 여부')


class GetUserResponseSchema(BaseModel):
    id: str = Field(..., description='사용자 id')
    name: str = Field(..., description='사용자 이름')
    gender: str = Field(..., description='성별')
    age: int = Field(..., description='나이')
    phone: str = Field(..., pattern=r'^010-\d{4}-\d{4}$', description='핸드폰 번호')
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', description='사용자 이메일(아이디)')
    is_admin: bool = Field(..., description='관리자 여부')


class GetUsersListResponseSchema(BaseModel):
    result: List[GetUserResponseSchema]


class ModifyUserRequestSchema(BaseModel):
    name: Optional[str] = Field(None, description='사용자 이름')
    gender: Optional[str] = Field(None, description='성별')
    age: Optional[int] = Field(None, description='나이')
    phone: Optional[str] = Field(None, pattern=r'^010-\d{4}-\d{4}$', description='핸드폰 번호')
    is_admin: Optional[bool] = Field(False, description='관리자 여부')


class ExceptionResponseSchema(BaseModel):
    error_code: str
    message: str


class RequestValidationExceptionResponseSchema(BaseModel):
    error_code: str
    message: str
