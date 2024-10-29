from fastapi import APIRouter

from api.user.user import user_router
from api.post.post import post_router
from api.account.account import account_router

router = APIRouter(prefix='/api/v1')
router.include_router(account_router, tags=['account'])
router.include_router(user_router, prefix='/users', tags=['user'])
router.include_router(post_router, prefix='/posts', tags=['post'])
