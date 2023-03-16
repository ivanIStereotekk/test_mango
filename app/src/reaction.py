from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.db import get_async_session
from app.models import User, Reaction
from app.schemas import ReactionCreate, ReactionResponse
from app.users import fastapi_users

current_user = fastapi_users.current_user(active=True)

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/add",
             status_code=status.HTTP_201_CREATED)
async def add_reaction(user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session),
                       reaction: ReactionCreate = Depends()):
    """
    Reaction add method - unique reaction
    :param user:
    :param session:
    :param reaction:
    :return: added entity
    """
    try:
        new_reaction = Reaction(user_id=user.id,
                                type=reaction.type,
                                message_id=reaction.message_id)
        # C H E C K  T H E   S A M E
        _statement = select(Reaction).where(Reaction.user_id ==
                                            user.id).where(Reaction.message_id == reaction.message_id)
        _results = await session.execute(_statement)
        from_db = _results.scalars().first()
        if from_db is None:
            session.add(new_reaction)
            await session.commit()
        return {"reaction": new_reaction}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get",
            response_model=ReactionResponse,
            status_code=status.HTTP_200_OK)
async def get_all_reactions(user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)):
    """
    Method to get all user reactions from the database.
    :param user:
    :param session:
    :return: Reactions
    """
    try:
        statement = select(Reaction).where(Reaction.user_id == user.id)
        results = await session.execute(statement)
        instances = results.scalars().all()

    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"reactions": instances}


@router.get("/get_by/{message_id}",
            response_model=ReactionResponse,
            status_code=status.HTTP_200_OK)
async def get_all_reactions_message_id(message_id: int, user: User = Depends(current_user),
                                       session: AsyncSession = Depends(get_async_session)):
    """
    Method to get all reactions by message id from the database.
    :param message_id:
    :param user:
    :param session:
    :return: Reactions                                          # SCHEMA NEED
    """
    if user.is_active:
        try:
            statement = select(Reaction).where(Reaction.message_id == message_id)
            results = await session.execute(statement)
            instances = results.scalars().all()

        except SQLAlchemyError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"reactions": instances}


@router.delete("/delete/{reaction_id}",
               status_code=status.HTTP_200_OK)
async def delete_reactions(reaction_id: int, user: User = Depends(current_user),
                           session: AsyncSession = Depends(get_async_session)):
    """
    Method to delete reaction from db {ONLY PERSONAL}.
    :param reaction_id: id of item to delete
    :param user:
    :param session:
    :return: Reactions
    """
    try:
        execution = await session.execute(
            select(Reaction).where(Reaction.id == reaction_id).where(Reaction.user_id == user.id))
        item = execution.scalars().first()
        if item is not None:
            await session.delete(item)
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail="Item not found")

        return {'details': "deleted successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
