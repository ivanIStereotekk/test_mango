from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from datetime import datetime
from app.models import User,Message
from app.db import get_async_session
from app.schemas import MessageResponse, MessageCreate
from app.users import fastapi_users

current_user = fastapi_users.current_user(active=True)

router = APIRouter(
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
                              chat_id=message.chat_id
                              )
        session.add(new_message)
        await session.commit()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"messages": [new_message]}


@router.get("/get",
            response_model=MessageResponse,
            status_code=status.HTTP_200_OK)
async def get_current_user_messages(user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    try:
        statement = select(Message).where(Message.author_id == user.id)
        results = await session.execute(statement)
        instances = results.scalars().all()
        return {"messages": instances}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get/{chat_id}",
            response_model=MessageResponse,
            status_code=status.HTTP_200_OK)
async def get_messages_by_chat_id(chat_id: int,user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    if user:
        try:
            statement = select(Message).where(Message.chat_id == chat_id)
            results = await session.execute(statement)
            instances = results.scalars().all()
            return {"messages": instances}

        except SQLAlchemyError as e:
            raise HTTPException(status_code=400, detail=str(e))
