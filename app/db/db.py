from pymongo import MongoClient
from app.db.models import Question, Answer
from bson import ObjectId


from app.core.config import DB_LINK, DB

client = MongoClient(DB_LINK)
db = client[DB]

questions = db['questions']
answers = db['answers']

def insert_question(question: Question):
    question_dict = question.dict()
    questions.insert_one(question_dict)

def get_question_by_id(question_id: str) -> Question:
    question_dict = questions.find_one({"_id": ObjectId(question_id)})
    return Question(**question_dict)

def insert_answer(answer: Answer):
    answer_dict = answer.dict()
    answers.insert_one(answer_dict)

def get_answer_by_id(answer_id: str) -> Answer:
    answer_dict = answers.find_one({"_id": ObjectId(answer_id)})
    return Answer(**answer_dict)

def get_answers_by_question_id(question_id: str):
    return answers.find({"question_id": question_id})
