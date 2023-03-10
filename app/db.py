from typing import AsyncGenerator, Optional
from sqlalchemy import Integer, String, ForeignKey, Text, Boolean, DateTime, Table, Column
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
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

# Association Table

class User(SQLAlchemyBaseUserTable[int], Base):
    """
    User table with obvious and visible fields and options.
    """
    __tablename__ = 'user_table'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    pictures: Mapped["Picture"] = relationship(backref='user',uselist=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=True, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    def __repr__(self):
        return f"User= {self.name} {self.surname} "


class Picture(Base):
    """
    Picture model wih a foreign key reference to a User model and picture saving options.
    """
    __tablename__ = "picture_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), nullable=False)
    file_50: Mapped[str] = mapped_column(Text)
    file_100: Mapped[str] = mapped_column(Text)
    file_400: Mapped[str] = mapped_column(Text)
    original: Mapped[str] = mapped_column(Text)
    # Picture.user - backref

    def __repr__(self):
        return f"Picture_id={self.id}, user={self.user_id})"


class Reaction(Base):
    """
    Reaction model - which shows user who reacted to a picture or chat message.
    Type field should contain the type of the reaction like "like" or "dislike".
    """
    __tablename__ = "reaction_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("message_table.id"), nullable=True)

    def __repr__(self):
        return f"Reaction_id={self.id}, user={self.user_id}, type={self.type}"


class Message(Base):
    """
    Message Table which contains text messages related to the chat and of course users who participating in the chat
    """
    __tablename__ = "message_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), nullable=True)
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(Text, nullable=False)
    reactions: Mapped["Reaction"] = relationship(backref='message',lazy='joined',uselist=True)
    chat_id: Mapped[int] = mapped_column(Integer,default=None)
    def __repr__(self):
        return f"Message_id={self.id}, author={self.author_id}, created_at={self.chat_id}"




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
