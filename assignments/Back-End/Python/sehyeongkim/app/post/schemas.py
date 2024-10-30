import datetime as dt
from typing import List
from pydantic import BaseModel, Field


class CreatePostRequestSchema(BaseModel):
    title: str = Field(..., description='게시글 제목')
    content: str = Field(..., description='게시글 본문')


class GetPostResponseSchema(BaseModel):
    id: int = Field(..., description='게시글 id')
    user_id: str = Field(..., description='게시글 업로드 유저 id')
    title: str = Field(..., description='게시글 제목')
    content: str = Field(..., description='게시글 본문')
    created_at: dt.datetime = Field(..., description='게시글 게시 날짜')


class GetPostsListResponseSchema(BaseModel):
    result: List[GetPostResponseSchema]


class ModifyPostRequestSchema(BaseModel):
    content: str = Field(..., description='게시글 내용')


class ExceptionResponseSchema(BaseModel):
    error_code: str
    message: str


class RequestValidationExceptionResponseSchema(BaseModel):
    error_code: str
    message: str
