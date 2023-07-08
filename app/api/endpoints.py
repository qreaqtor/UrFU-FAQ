from fastapi import FastAPI, Depends
from beanie import init_beanie
from typing import List
from app.core.security.auth import auth_backend, fastapi_users, current_active_user
from app.core.security.schemas import *

from app.api.moderate import get_moderate_question, get_moderate_answer, get_moderate_topic

###------- ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ -------###
from app.db.models import *
from app.db.db import *


app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )


### Создаёт новый вопрос
@app.post("/new_question")
async def create_question(question: QuestionIn, user = Depends(current_active_user)):
    topics = [x.title for x in await get_topics()]
    topic_title = get_moderate_topic(topics, question.content)
    topic = Topic(title=topic_title)
    topic_id = await get_question_topic_id(topic)
    result = Question(**question.dict(), user_id=user.id, topic_id=topic_id)
    await insert_question(result)

### Возвращает один вопрос
@app.get("/questions/{question_id}", response_model=QuestionOut)
async def get_question(question_id: str):
    return await get_question_by_id(question_id)

### Возвращает список всех вопросов
@app.get("/all_questions/{topic}", response_model=List[QuestionOut])
async def get_all_questions(topic: str):
    return await get_questions(topic_id=topic)

### Создаёт новый ответ
@app.post("/new_answer")
async def create_answer(answer: AnswerIn, user = Depends(current_active_user)):
    await insert_answer(Answer(**answer.dict(), user_id=user.id))

### Возвращает один ответ
@app.get("/answers/{answer_id}", response_model=AnswerOut)
async def get_answer(answer_id: str):
    return await get_answer_by_id(answer_id)

### Возвращает список всех ответов, которые являются ответом на вопрос question_id
@app.get("/all_answers/{question_id}", response_model=List[AnswerOut])
async def get_all_answers_by_question_id(question_id: str):
    return await get_answers_by_question_id(question_id)

### Возвращает список всех тем
@app.get("/all_topics/", response_model=List[TopicOut])
async def get_all_topics():
    return await get_topics()

@app.get("/moderate/question/{question}")
async def get_moderate_of_question(question: str):
    return get_moderate_question(question)

@app.get("/moderate/answer/{question}/{answer}")
async def get_moderate_of_answer(question: str, answer: str):
    return get_moderate_answer(answer, question)

@app.get("/moderate/topics/{topics}/{question}")
async def get_topic_by_question(topics: str, question: str):
    return get_moderate_topic(topics.split(','), question)
