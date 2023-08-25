
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String, ForeignKey, Text, Boolean, DateTime, Table, Column,LargeBinary
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column





class Base(DeclarativeBase):
    pass



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
    pictures: Mapped["Picture"] = relationship(backref='user', uselist=False)
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
    filename: Mapped[str] = mapped_column(Text,nullable=False)
    tag: Mapped[str] = mapped_column(String)
    # Picture.user - backref

    def __repr__(self):
        return f"Picture_id={self.id}, user={self.user_id} tag={self.tag})"


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
    reactions: Mapped["Reaction"] = relationship(backref='message', lazy='joined', uselist=True)
    chat_id: Mapped[int] = mapped_column(Integer, default=None)

    def __repr__(self):
        return f"Message_id={self.id}, author={self.author_id}, chat_id={self.chat_id}"



# class ContactList(Base):
#     "Продумай Контакт Лист и Методы ..."
#     __tablename__ = 'contact_table'
#     id: Mapped[int] = mapped_column(primary_key=True)

class Equipement(Base):
    """Equipment - item table which contains artists any kind of studio gear"""
    __tablename__ = "equipment_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(Text)
    model: Mapped[str] = mapped_column(Text)
    gear_type: Mapped[str] = mapped_column(Text)
    prod_year: Mapped[str] = mapped_column(Text)
    characteristics: Mapped[str] = mapped_column(Text)

    def __repr__(self):
        return f"Equipment_id={self.id}, brand={self.brand}, model={self.model}, type={self.gear_type}"




class Release(Base):
    """Release - table which contains artists album """
    __tablename__ = "release_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    artist: Mapped[str] = mapped_column(Text)
    genre: Mapped[str] = mapped_column(Text)
    release_date: Mapped[str] = mapped_column(Text)
    story_text: Mapped[str] = mapped_column(Text)
    record_label: Mapped[str] = mapped_column(Text)
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    cover_id: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f"release_id={self.id}, name={self.name}, artist={self.artist}, release_date={self.release_date}"