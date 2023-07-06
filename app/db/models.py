from datetime import datetime
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field

from beanie import Document
from fastapi_users.db import BeanieBaseUser
from pymongo.collation import Collation

class Question(BaseModel):
    user_id: str
    title: str
    text_content: str
    date_created: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = []
    was_checked: bool = False

class Answer(BaseModel):
    user_id: str
    question_id: str
    text_content: str
    date_created: datetime = Field(default_factory=datetime.utcnow)
    was_checked: bool = False

class User(BeanieBaseUser, Document):
    name: str
    surname: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Settings:
        name = "users"
        email_collation = Collation("en", strength=2)
