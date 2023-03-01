import uuid
from pydantic import validator, Field, BaseModel
from pydantic.types import constr
from fastapi_users import schemas
from typing import List
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

class PictureSchema(BaseModel):
    user_id: int
    file_50: str
    file_100: str
    file_400: str
    original: str

class ReactionSchema(BaseModel):
    id: int
    user_id: int
    type: str
    user: str
    reacted_message: str






class MessageSchema(BaseModel):
    id: int
    author_id: int
    body: str
    created_at: datetime
    reactions_ids: List[int] = []
    reactions: List[ReactionSchema]


class ChatSchema(BaseModel):
    id: int
    user_ids: List[int]
    message_ids: List[int]
    created_at: datetime
    text_messages: List[MessageSchema]







