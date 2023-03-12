from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, union_all
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy.orm import with_parent
from app.db import User, get_async_session, Chat
from app.schemas import ChatNewResponse, ChatCreate, ChatMessagesResponse
from app.users import fastapi_users
from sqlalchemy.orm import with_parent

current_user = fastapi_users.current_user(active=True)

router = APIRouter(
    # dependencies=[Depends(current_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/add",
             response_model=ChatNewResponse, response_model_exclude_unset=True,
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
    created_chat = None
    try:
        participants = []
        for one_id in chat.participants:
            statement = select(User).where(User.id == one_id)
            results = await session.execute(statement)
            participant = results.scalars().first()
            if participant:
                participants.append(participant)
            if len(participants) >= 2:
                new_chat = Chat(participants=participants,
                                created_at=datetime.now(),
                                )
                session.add(new_chat)
                created_chat = new_chat
    except SQLAlchemyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    await session.commit()
    if created_chat:
        return ChatNewResponse.from_orm(created_chat)
    else:
        raise HTTPException(status_code=404, detail=str("Could not create"))


# Checker for no repeat chat.
# async def chat_exists(user:current_user,participants: list, session: AsyncSession = Depends(get_async_session)):
#     try:
#         statement = select(Chat.id).where(Chat.participants.any(User.id == user.id))
#         results = await session.execute(statement)
#         chat_messages = results.scalars().all()

# НАДО ДОБАВИТЬ ! - Проверку есть ли чат в базе с такими же юзерами. Хотя пришла идея проще реализовать...

@router.get("/get",
            response_model=ChatMessagesResponse,
            status_code=status.HTTP_200_OK)
async def get_user_chats(user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    """
    Method to get all chat's from the database.
    :param user:
    :param session:
    :return: messages
    """
    # select(User).where(User.addresses.contains(a1)))
    try:
        # statement = select(Chat.messages).where(Chat.participants.any(User.id == user.id))
        statement = select(Chat).where(with_parent(user, User.chats))
        results = await session.execute(statement)
        chat_messages = results.scalars().all()
        return {'messages': chat_messages}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
