from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db import User, get_async_session, Reaction
from app.schemas import ReactionCreate, ReactionResponse
from app.users import fastapi_users

current_user = fastapi_users.current_user(active=True)

router = APIRouter(
    # dependencies=[Depends(current_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/add",
             response_model=ReactionResponse,
             status_code=status.HTTP_201_CREATED)
async def add_reaction(user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session),
                       reaction: ReactionCreate = Depends()):
    """
    Method to add a new picture to the database.
    :param reaction:
    :param user:
    :param session:
    :param picture:
    :return:
    """
    try:
        new_reaction = Reaction(user_id=user.id,
                                type=reaction.type,
                                reacted_message=reaction.reacted_message),

        session.add(new_reaction)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await session.commit()
    return {"reactions": new_reaction}


@router.get("/get",
            response_model=ReactionResponse,
            status_code=status.HTTP_200_OK)
async def get_reactions(user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)):
    """
    Method to get all pictures from the database.
    :param user:
    :param session:
    :return: Reactions
    """
    try:
        statement = select(Reaction).where(Reaction.user_id == user.id)
        results = await session.execute(statement)
        instances = results.scalars().all()
        return {"pictures": instances}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
