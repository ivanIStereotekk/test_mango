import uuid
from pydantic import validator, Field
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    name: str
    surname: str
    phone_number: str
    is_active: bool
    is_superuser: bool
    is_verified: bool



class UserCreate(schemas.BaseUserCreate):
    name: str
    surname: str
    phone_number: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)


    @validator('phone_number')
    def phone_must_contain_plus(cls, v):
        if '+7' not in v and len(v) < 10:
            raise ValueError('Phone number should start with + 7 and contain more than 10 digits')
        return v.title()


class UserUpdate(schemas.BaseUserUpdate):
    name: str
    surname: str
    phone_number: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)


ivan = {
  "email": "ivan.stereotekk@gmail.com",
  "password": "qwertyuiop123",
  "is_active": True,
  "is_superuser": False,
  "is_verified": False,
  "name": "Ivan",
  "surname": "Goncharov",
  "phone_number": "+79855203082"
}

john = {
  "email": "john@gmail.com",
  "password": "jonnydebth123",
  "is_active": True,
  "is_superuser": False,
  "is_verified": False,
  "name": "Johan",
  "surname": "Debth",
  "phone_number": "888898888"

}