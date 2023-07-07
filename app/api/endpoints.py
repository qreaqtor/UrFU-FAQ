from fastapi import FastAPI, Depends
from beanie import init_beanie
from app.core.security.auth import auth_backend, fastapi_users, current_active_user
from app.core.security.schemas import *

from app.api.moderate import get_moderate_question, get_moderate_answer

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
async def create_question(question: Question):
    await insert_question(question)

### Возвращает один вопрос
@app.get("/questions/{question_id}")
async def get_question(question_id: str):
    return await get_question_by_id(question_id)

### Создаёт новый ответ
@app.post("/new_answer")
async def create_answer(answer: Answer):
    await insert_answer(answer)

### Возвращает один ответ
@app.get("/answers/{answer_id}")
async def get_answer(answer_id: str):
    return await get_answer_by_id(answer_id)

### Возвращает список всех ответов, которые являются ответом на вопрос question_id
@app.get("/all_answers/{question_id}")
async def get_all_answers_by_question_id(question_id: str):
    answers = await get_answers_by_question_id(question_id)
    result = []
    async for answer in answers:
        result.append(Answer(**answer))
    return result

@app.get("/moderate/question/{question}")
async def get_moderate_of_question(question: str):
    return get_moderate_question(question)

@app.get("/moderate/answer/{question}/{answer}")
async def get_moderate_of_answer(question: str, answer: str):
    return get_moderate_answer(answer, question)
