from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from beanie import Document, PydanticObjectId
from fastapi_users.db import BeanieBaseUser
from pymongo.collation import Collation


class QuestionIn(BaseModel):
    question: str
    # date_created: datetime = Field(default_factory=datetime.utcnow)

class QuestionOut(BaseModel):
    id: PydanticObjectId
    user_id: PydanticObjectId
    topic_id: PydanticObjectId
    question: str
    date_created: datetime

class Question(BaseModel):
    user_id: PydanticObjectId
    topic_id: PydanticObjectId
    question: str
    date_created: datetime = Field(default_factory=datetime.utcnow)


class AnswerIn(BaseModel):
    question_id: PydanticObjectId
    answer: str
    # date_created: datetime = Field(default_factory=datetime.utcnow)

class AnswerOut(BaseModel):
    id: PydanticObjectId
    user_id: PydanticObjectId
    question_id: PydanticObjectId
    answer: str
    date_created: datetime

class Answer(BaseModel):
    user_id: PydanticObjectId
    question_id: PydanticObjectId
    answer: str
    date_created: datetime = Field(default_factory=datetime.utcnow)


class QuestionAndAnswerIn(BaseModel):
    question: str
    answer: str


class TopicOut(BaseModel):
    id: PydanticObjectId
    title: str

class Topic(BaseModel):
    title: str


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
