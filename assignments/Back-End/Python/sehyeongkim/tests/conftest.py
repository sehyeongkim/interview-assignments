import pytest
import asyncio
import pytest_asyncio
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, async_scoped_session

from tests.test_db_handler import TestDBHandler

test_db_handler = TestDBHandler()

async_engine = create_async_engine(test_db_handler.TEST_DB_URL.replace('pymysql', 'aiomysql'))
async_session_factory = async_sessionmaker(class_=AsyncSession, bind=async_engine, expire_on_commit=False)

@pytest.fixture(scope='session', autouse=True)
def initialize_database():
    test_db_handler.apply_alembic()
    yield

@pytest.yield_fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.yield_fixture(scope='session')
def crypto_context():
    context = CryptContext(schemes=['bcrypt'])
    yield context

@pytest.fixture(scope='function', autouse=True)
def init():
    data = test_db_handler.init_data()
    yield data
    test_db_handler.delete_all_rows()

@pytest_asyncio.fixture(scope='function', autouse=True)
async def session(mocker):
    """ Replace the testing db with the async session """
    async_session = async_scoped_session(session_factory=async_session_factory, scopefunc=asyncio.current_task)
    mocker.patch('core.db.transactional.session', async_session)
    mocker.patch('app.user.services.session', async_session)
    mocker.patch('app.post.services.session', async_session)
    yield async_session
    await async_session.remove()
