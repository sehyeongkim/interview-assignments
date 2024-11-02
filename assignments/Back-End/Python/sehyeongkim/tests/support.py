from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.models import User
from core.utils.token_helper import TokenHelper

NOT_FOUND_UUID = '46840c26-5e38-4967-8269-92572c71f588'

async def create_users(session: AsyncSession) -> dict:
    superuser_email = 'superuser@gmail.com'
    user_email = 'user@gmail.com'
    super_user = User(name='superuser',
                      email=superuser_email,
                      password='1234',
                      is_admin=True)
    normal_user = User(name='user',
                       email=user_email,
                       password='1234')
    session.add(super_user)
    session.add(normal_user)
    await session.commit()

    result1 = await session.execute(select(User).where(User.email == superuser_email))
    result2 = await session.execute(select(User).where(User.email == user_email))
    superuser = result1.scalars().first()
    user = result2.scalars().first()
    superuser_token = TokenHelper.encode(payload={'user_id': superuser.id_str})
    user_token = TokenHelper.encode(payload={'user_id': user.id_str})
    return {'superuser_id': superuser.id_str, 'superuser_token': superuser_token,
            'user_id': user.id_str, 'user_token': user_token}
