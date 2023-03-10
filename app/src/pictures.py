from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db import User, get_async_session, Picture
from app.schemas import PictureResponse, PictureCreate
from app.users import fastapi_users


current_user = fastapi_users.current_user(active=True)

router = APIRouter(
    dependencies=[Depends(current_user)],
    responses={404: {"description": "Not found"}},
)
@router.post("/add",
             response_model=PictureResponse,
             status_code=status.HTTP_201_CREATED)
async def add_picture(user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session),
                      picture: PictureCreate = Depends()):
    """
    Method to add a new message to the database.
    :param user:
    :param session:
    :param picture:
    :return:
    """
    try:
        new_picture = Picture(user_id=user.id,
                              file_50=picture.file_50,
                              file_100=picture.file_100,
                              file_400=picture.file_400,
                              original=picture.original
                              )
        session.add(new_picture)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await session.commit()
    return {"pictures": [
        PictureCreate.from_orm(new_picture)
    ]}


@router.get("/get",
            response_model=PictureResponse,
            status_code=status.HTTP_200_OK)
async def get_pictures(user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    """
    Method to get all messages from the database.
    :param user:
    :param session:
    :return:
    """
    try:
        statement = select(Picture).where(Picture.user_id == user.id)
        results = await session.execute(statement)
        instances = results.scalars().all()
        return {"pictures": instances}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
