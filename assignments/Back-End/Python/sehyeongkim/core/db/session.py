from contextvars import ContextVar, Token

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, async_scoped_session
from sqlalchemy.ext.declarative import declarative_base

from core.config import config

session_context = ContextVar('session_context')

def get_session_context() -> str:
    return session_context.get()

def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)

def reset_session_context(context: Token) -> None:
    session_context.reset(context)

engine = create_async_engine(f'mysql+aiomysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}', pool_recycle=3600)
async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    bind=engine,
    expire_on_commit=False,
)
session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)
Base = declarative_base()
