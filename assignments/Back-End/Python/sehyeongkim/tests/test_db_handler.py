from alembic import command
from sqlalchemy import text, inspect, create_engine, Engine
from alembic.config import Config as AlembicConfig

from core.config import config


class TestDBHandler:
    __test__ = True

    EXCLUDE_TABLES = {'alembic_version'}
    TEST_DB_URL = config.TEST_DB_URL.replace('aiomysql', 'pymysql')

    def apply_alembic(self) -> None:
        alembic_cfg = AlembicConfig('alembic.ini')
        alembic_cfg.set_main_option('is_testing', 'True')
        alembic_cfg.set_main_option('sqlalchemy.url', config.TEST_DB_URL.replace('aiomysql', 'pymysql'))
        command.upgrade(alembic_cfg, 'head')

    def delete_all_rows(self) -> None:
        engine = create_engine(url=self.TEST_DB_URL)
        tables = self._get_all_tables(engine=engine)
        for table in tables:
            if table in self.EXCLUDE_TABLES:
                continue
            with engine.begin() as conn:
                conn.execute(text(f'DELETE FROM {table}'))

    def drop_all(self) -> None:
        engine = create_engine(url=self.TEST_DB_URL)
        tables = self._get_all_tables(engine=engine)
        for table in tables:
            with engine.begin() as conn:
                conn.execute(text(f'DROP TABLE {table}'))

    def _get_all_tables(self, engine: Engine) -> list[str]:
        with engine.connect() as conn:
            inspector = inspect(conn)
            tables = inspector.get_table_names()
        return tables
