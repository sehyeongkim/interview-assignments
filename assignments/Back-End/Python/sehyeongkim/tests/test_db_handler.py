from alembic import command
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, text, inspect, create_engine, Engine
from alembic.config import Config as AlembicConfig

from app.user.models import User
from app.post.models import Post
from core.config import config
from core.utils.token_helper import TokenHelper


class TestDBHandler:
    __test__ = True

    EXCLUDE_TABLES = {'alembic_version'}
    ENGINE = create_engine(url=config.TEST_DB_URL.replace('aiomysql', 'pymysql'))

    def apply_alembic(self) -> None:
        alembic_cfg = AlembicConfig('alembic.ini')
        alembic_cfg.set_main_option('is_testing', 'True')
        alembic_cfg.set_main_option('sqlalchemy.url', config.TEST_DB_URL.replace('aiomysql', 'pymysql'))
        command.upgrade(alembic_cfg, 'head')

    def init_data(self) -> dict:
        superuser_email = 'superuser@gmail.com'
        user_email = 'user@gmail.com'

        local_session = sessionmaker(bind=self.ENGINE, autocommit=False, autoflush=False)
        with local_session() as session:
            super_user = User(name='superuser', email=superuser_email, password='1234', is_admin=True)
            normal_user = User(name='user', email=user_email, password='1234')
            session.add(super_user)
            session.add(normal_user)
            session.flush()
            session.refresh(super_user)
            session.refresh(normal_user)

            post = Post(title='제목', content='내용', user_id=normal_user.id)
            session.add(post)
            session.commit()
            session.refresh(post)

            user1 = session.execute(select(User).where(User.email==superuser_email))
            user2 = session.execute(select(User).where(User.email==user_email))
            superuser = user1.scalars().first()
            user = user2.scalars().first()

        superuser_token = TokenHelper.encode(payload={'user_id': superuser.id_str})
        user_token = TokenHelper.encode(payload={'user_id': user.id_str})
        return {'superuser_id': superuser.id_str, 'superuser_token': superuser_token,
                'user_id': user.id_str, 'user_token': user_token, 'post_id': post.id}


    def delete_all_rows(self) -> None:
        tables = self._get_all_tables(engine=self.ENGINE)
        for table in tables:
            if table in self.EXCLUDE_TABLES:
                continue
            with self.ENGINE.begin() as conn:
                conn.execute(text(f'DELETE FROM {table}'))

    def drop_all(self) -> None:
        tables = self._get_all_tables(engine=self.ENGINE)
        for table in tables:
            with self.ENGINE.begin() as conn:
                conn.execute(text(f'DROP TABLE {table}'))

    def _get_all_tables(self, engine: Engine) -> list[str]:
        with engine.connect() as conn:
            inspector = inspect(conn)
            tables = inspector.get_table_names()
        return tables
