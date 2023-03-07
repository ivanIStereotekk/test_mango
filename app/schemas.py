import uuid
from pydantic import validator, Field, BaseModel
from pydantic.types import constr
from fastapi_users import schemas
from typing import List, Optional
from datetime import datetime


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


class ReactionSchema(BaseModel):
    id: int = None
    user_id: int = None
    type: str
    user: str
    reacted_message: str


# Response schema


class MessageCreate(BaseModel):
    id: int = None
    author_id: int = None
    body: str
    created_at: Optional[datetime]
    class Config:
        orm_mode = True
class MessageRespInner(BaseModel):
    id: int
    author_id: int
    body: str
    created_at: Optional[datetime]
    reaction_ids: list
    reactions: list
    class Config:
        orm_mode = True
class MessageResponse(BaseModel):
    messages: list[MessageCreate]
    class Config:
        orm_mode = True

class ChatSchema(BaseModel):
    id: int
    user_ids: list[int]
    message_ids: list[int]
    created_at: datetime
    text_messages: list[MessageResponse]
