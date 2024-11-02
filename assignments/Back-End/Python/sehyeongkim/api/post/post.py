from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.post.schemas import CreatePostRequestSchema, GetPostResponseSchema, GetPostsListResponseSchema, ModifyPostRequestSchema
from app.post.services import PostService
from core.fastapi.dependencies.permission import PermissionDependency, IsPostOwner, IsAuthenticated

post_router = APIRouter()


@post_router.get(
    '',
    response_model=GetPostsListResponseSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def get_posts_list():
    result = await PostService().get_posts()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@post_router.post(
    '',
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def create_post(request: Request, create_post_request: CreatePostRequestSchema):
    post_info = dict(create_post_request)
    post = await PostService().insert_post(request.user.id, post_info)
    return JSONResponse(content={'result': 'success', 'post_id': post.id}, status_code=200)


@post_router.get(
    '/{post_id}',
    response_model=GetPostResponseSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def get_post(post_id: int):
    pass


@post_router.put(
    '/{post_id}',
    dependencies=[Depends(PermissionDependency([IsPostOwner]))]
)
async def modify_post(post_id: int, modify_post_request: ModifyPostRequestSchema):
    pass
