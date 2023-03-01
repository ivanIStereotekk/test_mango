import uuid
from pydantic import validator, Field
from pydantic.types import constr
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


# ivan = {
#   "email": "ivan.stereotekk@gmail.com",
#   "password": "qwertyuiop123",
#   "is_active": True,
#   "is_superuser": False,
#   "is_verified": False,
#   "name": "Ivan",
#   "surname": "Goncharov",
#   "phone_number": "+79855203082"
# }
#
# john = {
#   "email": "john@gmail.com",
#   "password": "jonnydebth123",
#   "is_active": true,
#   "is_superuser": false,
#   "is_verified": false,
#   "name": "Johan",
#   "surname": "Debth",
#   "phone_number": "888898888"
#
# }