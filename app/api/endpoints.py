from fastapi import FastAPI, Depends, HTTPException, Request
from beanie import init_beanie
from typing import List, Union

import openai
from app.core.security.auth import auth_backend, fastapi_users, current_active_user
from app.core.security.schemas import *

from app.api.moderate import get_moderate_question, get_moderate_answer, get_moderate_topic

###------- ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ -------###
from app.db.models import *
from app.db.db import *

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

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


### Создаёт новый вопрос, если он прошел модерацию, иначе возвращает список не удовлетворяющих критериев
@app.post("/new_question", response_model= Union[QuestionOut, List[str]])
async def create_question(question: QuestionIn, user = Depends(current_active_user)):
    try:
        moderate_response = get_moderate_question(question.question)
    except openai.error.RateLimitError as e:
        raise HTTPException(status_code=429, detail=str(e))
    if moderate_response:
        return moderate_response
    topics = [x.title for x in await get_topics()]
    topic_title = get_moderate_topic(topics, question.question)
    topic = await get_topic(Topic(title=topic_title))
    result = Question(**question.dict(), user_id=user.id, topic_id=topic.id)
    return await insert_question(result)

### Создаёт новый ответ, если он прошел модерацию, иначе возвращает список не удовлетворяющих критериев
@app.post("/new_answer", response_model= Union[AnswerOut, List[str]])
async def create_answer(answer: AnswerIn, user = Depends(current_active_user)):
    question = await get_question_by_id(answer.question_id)
    try:
        moderate_response = get_moderate_answer(answer.answer, question.question)
    except openai.error.RateLimitError as e:
        raise HTTPException(status_code=429, detail=str(e))
    if moderate_response:
        return moderate_response
    result = Answer(**answer.dict(), user_id=user.id)
    return await insert_answer(result)

### Создаёт новый вопрос и  ответ, если они прошли модерацию, иначе возвращает список не удовлетворяющих критериев
@app.post("/new_question_answer/", response_model= Union[QuestionAndAnswerOut, List[str]])
async def create_question_and_answer(q_and_a: QuestionAndAnswerIn, user = Depends(current_active_user)):
    try:
        question_response = get_moderate_question(q_and_a.question)
        answer_response = get_moderate_answer(q_and_a.answer, q_and_a.question)
    except openai.error.RateLimitError as e:
        raise HTTPException(status_code=429, detail=str(e))
    if question_response or answer_response:
        return question_response + answer_response
    topics = [x.title for x in await get_topics()]
    topic_title = get_moderate_topic(topics, q_and_a.question)
    topic = await get_topic(Topic(title=topic_title))
    question = await insert_question(Question(**q_and_a.dict(), user_id=user.id, topic_id=topic.id))
    answer = await insert_answer(Answer(**q_and_a.dict(), user_id=user.id, question_id=question.id))
    return QuestionAndAnswerOut(**answer.dict(), answer_id=answer.id, question=question.question)

# ### Возвращает один вопрос
# @app.get("/questions/{question_id}", response_model=QuestionOut)
# async def get_question(question_id: str):
#     return await get_question_by_id(question_id)

### Возвращает список всех вопросов в теме topic_id
@app.get("/questions_by_topic/{topic_id}", response_model=List[QuestionOut])
async def get_all_questions_by_topic(topic_id: str):
    return await get_questions(topic_id)

### Возвращает список всех вопросов, которые не имеют ответа
@app.get("/questions_without_answer/", response_model=List[QuestionOut])
async def get_all_questions_without_answer():
    return await get_questions_without_answer()

# ### Возвращает один ответ
# @app.get("/answers/{answer_id}", response_model=AnswerOut)
# async def get_answer(answer_id: str):
#     return await get_answer_by_id(answer_id)

### Возвращает список всех ответов, которые являются ответом на вопрос question_id
@app.get("/all_answers/{question_id}", response_model=List[AnswerOut])
async def get_all_answers_by_question_id(question_id: str):
    return await get_answers_by_question_id(question_id)

### Возвращает список всех тем
@app.get("/all_topics/", response_model=List[TopicOut])
async def get_all_topics():
    return await get_topics()

# ### Возвращает список из 1 и 0, где 1 с индексом i - соответствие критерию i
# @app.get("/moderate/question/{question}")
# async def get_moderate_of_question(question: str):
#     return get_moderate_question(question)

# ### Возвращает список из 1 и 0, где 1 с индексом i - соответствие критерию i
# @app.get("/moderate/answer/{question}/{answer}")
# async def get_moderate_of_answer(question: str, answer: str):
#     return get_moderate_answer(answer, question)

# @app.get("/moderate/topics/{topics}/{question}")
# async def get_topic_by_question(topics: str, question: str):
#     return get_moderate_topic(topics.split(','), question)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})
