import uuid
from pydantic import validator, Field, BaseModel
from pydantic.types import constr
from fastapi_users import schemas
from typing import List, Optional, Dict
from datetime import datetime

from sqlalchemy import null


# USER schemas

class UserRead(schemas.BaseUser[int]):
    name: str
    surname: str
    phone_number: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreate(schemas.BaseUserCreate):
    name: str
    surname: str
    phone_number: constr(strip_whitespace=True, min_length=8, max_length=15, regex="^\\+?[1-9][0-9]{7,14}$")
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)


class UserUpdate(schemas.BaseUserUpdate):
    name: str
    surname: str
    phone_number: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)


# Other Schemas
#    ================================================================= Picture

class PictureCreate(BaseModel):
    user_id: int = None
    file_50: str
    file_100: str
    file_400: str
    original: str

    class Config:
        orm_mode = True


class PictureResponse(BaseModel):
    pictures: list[PictureCreate]

    class Config:
        orm_mode = True


#    ================================================================= Reaction
class ReactionCreate(BaseModel):
    id: int = None
    user_id: Optional[int] = None
    type: str
    reacted_message: Optional[int] = None

    class Config:
        orm_mode = True


class ReactionResponse(BaseModel):
    reactions: ReactionCreate

    class Config:
        orm_mode = True


# Response schema
#    ================================================================= Message
class MessageCreate(BaseModel):
    id: int = None
    author_id: int = None
    body: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class MessageResponse(BaseModel):
    messages: list[MessageCreate]

    class Config:
        orm_mode = True


#    ================================================================= Chat


# id: Mapped[int] = mapped_column(primary_key=True)
# messages: Mapped[List[Message]] = relationship(secondary=message_association_table, lazy='joined')
# created_at: Mapped[str] = mapped_column(DateTime, nullable=False)
# participants: Mapped[List[User]] = relationship(secondary=chat_association_table, lazy='joined')

class ChatCreate(BaseModel):
    participants: Optional[List[int]]
    created_at: Optional[datetime] = None
class ChatResponse(BaseModel):
    id: int
    created_at: datetime
    messages: List[MessageResponse]
    participants: List[UserRead]
    class Config:
        orm_mode = True
