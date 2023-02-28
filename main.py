import uvicorn
from fastapi import Depends, FastAPI

from app.db import User, create_db_and_tables
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users

app = FastAPI(title="Messanger Mango Project", version="0.1.0")

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


@app.get("/authenticated-route",tags=["Authenticated Route GET PICTURES"])
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="info")
