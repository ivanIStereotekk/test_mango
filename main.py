from typing import List, Any

import uvicorn
from fastapi import Depends, FastAPI, APIRouter, HTTPException
from starlette import status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import PictureCreate, PictureResponse
from sqlalchemy import select

from app.db import User, create_db_and_tables, drop_db_and_tables, Picture
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users
from settings import SENTRY_DSN, SENTRY_TRACES_SAMPLE_RATE
import sentry_sdk
from app.db import get_async_session
from app.src.pictures import router
# Logging and Tracing With Sentry
sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
    instrumenter=None,
)

app = FastAPI(title="Messanger Mango Project", version="0.1.0")

# AUTHENTICATION ROUTERS

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["Authentication Token Methods"]
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
# Pictures Router
app.include_router(router, prefix="/pictures", tags=["Pictures API"])

# OTHER ROUTERS AND ENDPOINTS

current_user = fastapi_users.current_user(active=True)


@app.post("/drop_all/", tags=["For development usage only - DROP ALL / CREATE ALL TABLES DB"])
async def drop_route(command: str):
    if command == 'drop_all':
        await drop_db_and_tables()
        return {"Message": "Database and tables dropped"}
    if command == 'create_all':
        await create_db_and_tables()
        return {"Message": "Database and new tables migrated"}


@app.get("/current_user", tags=["Get Current user Method"])
def get_current_user(user: User = Depends(current_user)):
    return f"Hello, {user.id} email ={user.email} phone={user.phone_number}"


# @app.on_event("startup")
# async def on_startup():
#     await create_db_and_tables()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="info")
