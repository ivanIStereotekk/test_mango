
import uvicorn
from fastapi import Depends, FastAPI


from app.models import User


from app.db import create_db_and_tables, drop_db_and_tables, drop_table
from app.schemas import UserCreate, UserRead, UserUpdate, UserLogin
from app.users import auth_backend, current_active_user, fastapi_users
from settings import SENTRY_DSN, SENTRY_TRACES_SAMPLE_RATE
import sentry_sdk
from app.db import get_async_session
# R O U T E R S
from app.src.pictures import router as pictures_router
from app.src.reaction import router as reaction_router
from app.src.message import router as message_router
from app.src.chatgpt import router as chat_gpt_router
from app.src.soсketpoint import router as socket_router

# S E N T R Y - Tracing
sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
    instrumenter=None,
)

app = FastAPI(title="Messanger Mango Project", version="0.1.0")

# AUTHENTICATION ROUTERS


# CHANGED vs UserLogin
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["Login / Logout Methods"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Register User Method"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Reset Password Methods"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["Request Verify Token Methods"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["User Retrieve Methods"],
)
# D B  Entity's Routers
app.include_router(pictures_router, prefix="/pictures", tags=["User Pictures API"])
app.include_router(reaction_router, prefix="/reactions", tags=["User Reaction API"])
app.include_router(message_router, prefix="/private", tags=["Message API"])
app.include_router(chat_gpt_router, prefix="/prompt", tags=["Chat GPT API"])
app.include_router(socket_router, prefix="/socket", tags=["Web Socket API"])


# OTHER ROUTERS AND ENDPOINTS

current_user = fastapi_users.current_user(active=True)


@app.post("/drop_all/", tags=["For development usage only - DROP ALL / CREATE ALL TABLES DB"])
async def drop_route(command: str):
    match command:
        case "drop_all":
            await drop_db_and_tables()
            return {"Message": "Database and tables dropped"}
        case "create_all":
            await create_db_and_tables()
            return {"Message": "Database and new tables migrated"}
        case _:
            await drop_table(table_name=command)
            return {"Message": "You are right man! No need anymore this useless table...!"}


@app.get("/current_user", tags=["Get Current user Method"])
def get_current_user(user: User = Depends(current_user)):
    return f"Hello, {user.id} email ={user.email} phone={user.phone_number}"


# @app.on_event("startup")
# async def on_startup():
#     await create_db_and_tables()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="info")
