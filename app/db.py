from typing import AsyncGenerator
from sqlalchemy import Integer, Column, String, ForeignKey, Text,Boolean
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped
from typing import List

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from settings import PG_HOST, PG_PORT, PG_USER, PG_PASS, PG_DB_NAME


# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"

DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(30))
    surname: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String, nullable=False)
    phone_number: Mapped[str] = Column(String, nullable=False)
    hashed_password: Mapped[str] = Column(String, nullable=False)
    pictures: Mapped[List["Picture"]] = relationship(back_populates="picture_user_id")
    is_active: Mapped[bool] = Column(Boolean, nullable=True)
    is_superuser: Mapped[bool] = Column(Boolean, nullable=True)
    is_verified: Mapped[bool] = Column(Boolean, nullable=True)

    def __repr__(self):
        return f"User= {self.name} {self.surname} "


class Picture(Base):
    __tablename__ = "picture"
    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("user.id"), nullable=False)
    file_50: Mapped[str] = Column(Text)
    file_100: Mapped[str] = Column(Text)
    file_400: Mapped[str] = Column(Text)

    def __repr__(self):
        return f"Picture={self.id}, user={self.user_id})"


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_picture_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, Picture)