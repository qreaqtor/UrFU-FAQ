from beanie import PydanticObjectId
from fastapi_users import schemas
from fastapi_users import models
from pydantic import EmailStr


class UserRead(schemas.BaseUser[PydanticObjectId]):
    id: models.ID
    name: str
    surname: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    name: str
    surname: str
    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    name: str
    surname: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False