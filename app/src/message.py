from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from datetime import datetime
from app.db import User, get_async_session, Picture, Message
from app.schemas import PictureResponse, PictureCreate, MessageResponse, MessageCreate
from app.users import fastapi_users

current_user = fastapi_users.current_user(active=True)

router = APIRouter(
    # dependencies=[Depends(current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/add",
             response_model=MessageResponse,response_model_exclude_unset=True,
             status_code=status.HTTP_201_CREATED)
async def add_message(user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session),
                      message: MessageCreate = Depends()):
    try:
        new_message = Message(author_id=user.id,
                              body=message.body,
                              created_at=str(datetime.now()),
                              )
        session.add(new_message)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await session.commit()
    return {"messages": [new_message]}


@router.get("/get",
            response_model=MessageResponse,
            status_code=status.HTTP_200_OK)
async def get_messages(user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    try:
        statement = select(Message).where(Message.author_id == user.id)
        results = await session.execute(statement)
        instances = results.scalars().all()
        return {"messages": instances}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
