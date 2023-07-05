from fastapi import FastAPI, Depends
from beanie import init_beanie
from app.core.security.auth import auth_backend, fastapi_users, current_active_user
from app.core.security.schemas import *
from app.db.models import User


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


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )


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
