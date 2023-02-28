from typing import AsyncGenerator
from sqlalchemy import Integer, Column, String, ForeignKey, Text,Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped,mapped_column
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
    __tablename__ = 'user_table'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    pictures: Mapped[List["Picture"]] = relationship()
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=True, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    def __repr__(self):
        return f"User= {self.name} {self.surname} "


class Picture(Base):
    __tablename__ = "picture_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_table.id"), nullable=False)
    file_50: Mapped[str] = mapped_column(Text)
    file_100: Mapped[str] = mapped_column(Text)
    file_400: Mapped[str] = mapped_column(Text)
    original: Mapped[str] = mapped_column(Text)

    def __repr__(self):
        return f"Picture_id={self.id}, user={self.user_id})"

class Chat(Base):
    __tablename__ = "chat_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    users: Mapped[List["User"]] = mapped_column(Integer, ForeignKey("user_table.id"), nullable=True)
    messages: Mapped[List["Message"]] = mapped_column(Integer, ForeignKey("message_table.id"))
    created_at: Mapped[str] = mapped_column(DateTime, nullable=False)

    def __repr__(self):
        return f"Chat_id={self.id}, users={self.users}, created_at={self.created_at})"



class Reaction(Base):
    __tablename__ = "reaction_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user: Mapped[int] = mapped_column(Integer, ForeignKey("user_table.id"))
    type: Mapped[str] = mapped_column(String,nullable=True)
    def __repr__(self):
        return f"Reaction_id={self.id}, user={self.user}, type={self.type}"



class Message(Base):
    __tablename__ = "message_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author: Mapped[int] = mapped_column(Integer, ForeignKey("user_table.id"), nullable=False)
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(Text, nullable=False)
    reactions: Mapped[List["Reaction"]] = relationship(back_populates="type")
    def __repr__(self):
        return f"Message_id={self.id}, author={self.author}, created_at={self.created_at})"

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