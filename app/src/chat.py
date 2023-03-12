from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select,union_all
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy.orm import with_parent
from app.db import User, get_async_session, Chat
from app.schemas import ChatResponse, ChatCreate
from app.users import fastapi_users

current_user = fastapi_users.current_user(active=True)

router = APIRouter(
    # dependencies=[Depends(current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/add",
             status_code=status.HTTP_201_CREATED)
async def add_chat(user: User = Depends(current_user),
                   session: AsyncSession = Depends(get_async_session),
                   chat: Chat = Depends(ChatCreate)):
    """
    Method to add a new chat to the database.
    :param user:
    :param session:
    :param chat:
    :return: status.HTTP_201_CREATED
    results = await session.execute(statement)
    instances = results.scalars().all()
    """
    try:
        participants = []
        for one_id in chat.participants:
            print('one_id', one_id)
            statement = select(User).where(User.id == one_id)
            results = await session.execute(statement)
            participant = results.scalars().first()
            participants.append(participant)
        new_chat = Chat(participants=participants,
                        created_at=datetime.now(),
                        )
        session.add(new_chat)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await session.commit()
    return {"created": participants}


@router.get("/get",
            # response_model=ChatResponse,
            status_code=status.HTTP_200_OK)
async def get_chats(user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):
    """
    Method to get all chat's from the database.
    :param user:
    :param session:
    :return:
    """
# REED IT !!! - https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html#exists-forms-has-any


    try:
        # stm = select(User).where(User.id == user.id)
        # usr_result = await session.execute(stm)
        # participant = usr_result.scalars().first()
        statement = select(Chat.messages).where(Chat.participants.any(User.id == user.id))
        results = await session.execute(statement)
        chat_messages = results.scalars().all()
        return {'messages': chat_messages}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))


