import re
import motor.motor_asyncio
from app.db.models import Question, QuestionOut, Answer, AnswerOut, Topic, TopicOut
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
topics = db['topics']

async def insert_question(question: Question) -> QuestionOut:
    question_dict = question.dict()
    await questions.insert_one(question_dict)
    return QuestionOut(**question_dict, id=question_dict['_id'])

async def get_question_by_id(question_id: str) -> QuestionOut:
    question_dict = await questions.find_one({"_id": ObjectId(question_id)})
    return QuestionOut(**question_dict, id=question_dict['_id'])

async def get_questions(topic_id: str) -> List[QuestionOut]:
    result = []
    async for question in questions.find({"topic_id": ObjectId(topic_id)}):
        result.append(QuestionOut(**question, id=question['_id']))
    return result

async def get_questions_without_answer() -> List[QuestionOut]:
    result = []
    async for question in questions.find({"has_answer": False}):
        result.append(QuestionOut(**question, id=question['_id']))
    return result

async def insert_answer(answer: Answer) -> AnswerOut:
    answer_dict = answer.dict()
    await answers.insert_one(answer_dict)
    questions.update_one(
        {"_id": ObjectId(answer_dict['question_id'])},
        {"$set": {"has_answer": True}})
    return AnswerOut(**answer_dict, id=answer_dict['_id'])

async def get_answer_by_id(answer_id: str) -> AnswerOut:
    answer_dict = await answers.find_one({"_id": ObjectId(answer_id)})
    return AnswerOut(**answer_dict, id=answer_dict['_id'])

async def get_answers_by_question_id(question_id: str) -> List[AnswerOut]:
    result = []
    async for answer in answers.find({"question_id": ObjectId(question_id)}):
        result.append(AnswerOut(**answer, id=answer['_id']))
    return result

async def get_topics() -> List[TopicOut]:
    result = []
    async for topic in topics.find():
        result.append(TopicOut(**topic, id=topic['_id']))
    return result

async def get_topic(topic: Topic) -> TopicOut:
    topic_dict = await topics.find_one_and_update(
        {'title': topic.title},
        {'$setOnInsert': topic.dict()},
        upsert=True,
        return_document=True
    )
    return TopicOut(**topic_dict, id=topic_dict['_id'])

async def get_search_result(text: str):
    questions_result = []
    async for question in questions.find({"question":{"$regex":re.compile(text, re.IGNORECASE)}}):
        questions_result.append(QuestionOut(**question, id=question['_id']))
    return questions_result

async def get_all_answers_from_bd():
    result = []
    async for answer in answers.find():
        result.append(AnswerOut(**answer, id=answer['_id']))
    return result

async def get_all_questions_from_bd():
    result = []
    async for question in questions.find():
        result.append(QuestionOut(**question, id=question['_id']))
    return result

async def get_user_db():
    yield BeanieUserDatabase(User)
