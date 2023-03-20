import logging
import tempfile

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from PIL import Image

from starlette.responses import FileResponse
import shutil
from app.models import User, Picture
from app.users import fastapi_users
from app.db import get_async_session
from settings import root_dir

# Logger configuration
logging.basicConfig(filename=f'{root_dir}/logs/picture_logger.log', encoding='utf-8', level=logging.INFO)

current_user = fastapi_users.current_user(active=True)

router = APIRouter(
    dependencies=[Depends(current_user)],
    responses={404: {"description": "Not found"}},
)



@router.post("/add",
             status_code=status.HTTP_201_CREATED)
async def add_picture(tag: str, picture: UploadFile = File(),
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    """ Add file and image response"""

    with open(f"./static/pics/{picture.filename}", "wb+") as buff:
        shutil.copyfileobj(picture.file, buff)
        try:
            new = Picture(user_id=user.id,
                          filename=str(buff.name),
                          tag=tag)
            session.add(new)
            await session.commit()
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemyError: >> {e} \n {add_picture.__name__}")
            raise HTTPException(status_code=400, detail=str(e))
        logging.info(f"Added picture by {user.email} >> {picture.filename}")
        return {"details": f"{status.HTTP_201_CREATED, buff.name} Successfully added"}


@router.get("/get/{picture_id}",
            status_code=status.HTTP_200_OK)
async def get_pictures(picture_id: int, user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    """
    Method to get all messages from the database.
    :param user:
    :param session:
    :return:
    """
    try:
        statement = select(Picture).where(Picture.id == picture_id)
        results = await session.execute(statement)
        instance = results.scalars().first()
        if instance:
            return FileResponse(str(instance.filename), media_type="image/png")
        else:
            return {"details": f"{status.HTTP_404_NOT_FOUND} NOT FOUND"}
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: >> {e} \n {get_pictures.__name__}")
        raise HTTPException(status_code=400, detail=str(e))
@router.post("/get_size",
             status_code=status.HTTP_200_OK)
async def get_by_size_and_id(picture_id:int,size_h:int, size_v:int,user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    """ Method which returns resized picture"""
    try:
        statement = select(Picture).where(Picture.id == picture_id)
        results = await session.execute(statement)
        instance = results.scalars().first()
        if instance:
            img = Image.open(instance.filename)
            img_resize = img.resize((size_h, size_v))
            with open(f"./static/pics/resized.png", "wb+") as buff:
                img_resize.save(buff)
            return FileResponse(str(buff.name), media_type="image/png")
        else:
            return {"details": f"{status.HTTP_404_NOT_FOUND} NOT FOUND"}
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: >> {e} \n {get_pictures.__name__}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{picture_id}",
               status_code=status.HTTP_200_OK)
async def delete_picture(picture_id: int, user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    """
    Method to get all messages from the database.
    :param user:
    :param session:
    :return:
    """
    try:
        statement = select(Picture).where(Picture.id == picture_id)
        results = await session.execute(statement)
        instance = results.scalars().first()
        if instance:
            await session.delete(instance)
            await session.commit()
            return {"details": f"{status.HTTP_200_OK} Successfully deleted"}
        else:
            return {"details": f"{status.HTTP_404_NOT_FOUND} Not found"}

    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: >> {e} \n {delete_picture.__name__}")
        raise HTTPException(status_code=400, detail=str(e))


