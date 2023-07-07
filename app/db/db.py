import motor.motor_asyncio
from app.db.models import Question, QuestionOut, Answer, AnswerOut
from bson import ObjectId
from fastapi_users.db import BeanieUserDatabase
from typing import List
from app.db.models import User
from app.core.config import DB_LINK, DB

client = motor.motor_asyncio.AsyncIOMotorClient(
    DB_LINK, uuidRepresentation="standard"
)
db = client[DB]

users = db['users']
questions = db['questions']
answers = db['answers']

async def insert_question(question: Question):
    question_dict = question.dict()
    await questions.insert_one(question_dict)

async def get_question_by_id(question_id: str) -> QuestionOut:
    question_dict = await questions.find_one({"_id": ObjectId(question_id)})
    return QuestionOut(**question_dict, id=question_dict['_id'])

async def get_questions() -> List[QuestionOut]:
    result = []
    async for question in questions.find():
        result.append(QuestionOut(**question, id=question['_id']))
    return result

async def insert_answer(answer: Answer):
    answer_dict = answer.dict()
    await answers.insert_one(answer_dict)

async def get_answer_by_id(answer_id: str) -> AnswerOut:
    answer_dict = await answers.find_one({"_id": ObjectId(answer_id)})
    return AnswerOut(**answer_dict, id=answer_dict['_id'])

async def get_answers_by_question_id(question_id: str) -> List[AnswerOut]:
    result = []
    async for answer in answers.find({"question_id": ObjectId(question_id)}):
        result.append(AnswerOut(**answer, id=answer['_id']))
        print(answer)
    return result

async def get_user_db():
    yield BeanieUserDatabase(User)
