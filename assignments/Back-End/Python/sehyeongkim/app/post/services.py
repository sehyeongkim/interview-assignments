from core.db.session import session
from core.db.transactional import Transactional


class PostService:
    def __init__(self):
        pass

    @Transactional()
    async def insert_post(self):
        pass

    async def get_posts(self):
        pass

    @Transactional()
    async def update_post(self):
        pass

    async def is_post_owner(self):
        pass
