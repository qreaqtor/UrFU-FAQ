from datetime import datetime
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field

class Question(BaseModel):
    user_id: str
    title: str
    text_content: str
    date_created: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = []

class Answer(BaseModel):
    user_id: str
    question_id: str
    text_content: str
    date_created: datetime = Field(default_factory=datetime.utcnow)
