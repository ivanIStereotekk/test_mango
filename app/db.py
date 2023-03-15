from typing import AsyncGenerator

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from app.models import User
from app.models import Base
from fastapi import Depends


from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from settings import PG_HOST, PG_PORT, PG_USER, PG_PASS, PG_DB_NAME


DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"





engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def drop_table(table_name):
    async with engine.begin() as conn:
        statement = f"DROP TABLE {table_name}"
        await conn.execute(statement)


# Async Session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    BASIC GET_DATABASE CALLBACK
    :returns: or yields session !
    """
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
