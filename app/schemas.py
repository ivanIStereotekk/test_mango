from pydantic import Field, BaseModel
from pydantic.types import constr
from fastapi_users import schemas
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from datetime import date, datetime, time, timedelta

# USER schemas





class UserRead(schemas.BaseUser[int]):
    name: str
    surname: str
    email: str
    phone_number: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreate(schemas.BaseUserCreate):
    name: str
    email: EmailStr
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
class ReleaseCreate(BaseModel):
    id: int = None
    name: str = None
    artist: str = None
    genre: str = None
    release_date: datetime = None
    story_text: str = None
    record_label: str = None
    filename: str = None
    cover_id: int = None
    class Config:
        orm_mode = True





#    ================================================================= Reaction
class ReactionCreate(BaseModel):
    id: int = None
    user_id: int = None
    type: str
    message_id: int

    class Config:
        orm_mode = True


class ReactionInner(BaseModel):
    id: int
    user_id: int
    type: str
    message_id: int

    class Config:
        orm_mode = True


class ReactionResponse(BaseModel):
    reactions: list[ReactionInner]

    class Config:
        orm_mode = True


# Response schema
#    ================================================================= Message
class MessageCreate(BaseModel):
    id: int = None
    author_id: int = None
    body: str
    created_at: Optional[datetime]
    chat_id: int

    class Config:
        orm_mode = True


class MessageResponse(BaseModel):
    messages: list[MessageCreate]

    class Config:
        orm_mode = True


class GPT_Engines(BaseModel):
    engines: list