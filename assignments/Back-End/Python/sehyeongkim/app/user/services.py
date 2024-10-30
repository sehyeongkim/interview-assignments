from core.db.session import session
from core.db.transactional import Transactional


class UserService:
    def __init__(self):
        pass

    @Transactional()
    async def insert_user(self):
        pass

    async def get_users(self):
        pass

    @Transactional()
    async def update_user(self):
        pass

    @Transactional()
    async def delete_user(self):
        pass

    async def is_admin(self):
        pass
