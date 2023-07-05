from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



###------- ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ -------###
from app.db.models import *
from app.db.db import *

### Создаёт новый вопрос
@app.post("/new_question")
async def create_question(question: Question):
    insert_question(question)

### Возвращает один вопрос
@app.get("/questions/{question_id}")
async def get_question(question_id: str):
    return get_question_by_id(question_id)

### Создаёт новый ответ
@app.post("/new_answer")
async def create_answer(answer: Answer):
    insert_answer(answer)

### Возвращает один ответ
@app.get("/answers/{answer_id}")
async def get_answer(answer_id: str):
    return get_answer_by_id(answer_id)

### Возвращает список всех id ответов, которые являются ответом на вопрос question_id
@app.get("/all_answers/{question_id}")
async def get_answers_ids_by_question_id(question_id: str) -> List[str]:
    answers = get_answers_by_question_id(question_id)
    return [str(answer["_id"]) for answer in answers]
