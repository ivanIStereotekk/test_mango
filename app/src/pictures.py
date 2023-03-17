import base64
import io
import json
import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
import os, sys
from PIL import Image
import tempfile
from starlette.responses import FileResponse, StreamingResponse
import shutil

from app.models import User, Picture
from app.users import fastapi_users
from app.db import get_async_session
from settings import root_dir

current_user = fastapi_users.current_user(active=True)

router = APIRouter(
    dependencies=[Depends(current_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/add",
             status_code=status.HTTP_201_CREATED)
async def add_picture(tag: str,picture: UploadFile = File(),
                   user: User = Depends(current_user),
                   session: AsyncSession = Depends(get_async_session)):
    """ Add file and image response"""
    with open(f"./temp/temporary.png","wb+") as buff:
        shutil.copyfileobj(picture.file,buff)
        string_b = base64.b64encode(buff.read())
        new = Picture(user_id=user.id,
                      picture=string_b,
                      tag=tag)
        session.add(new)
        await session.commit()
        return {"details":f"{status.HTTP_201_CREATED} Successfully added"}


@router.get("/get/{picture_id}",
            status_code=status.HTTP_200_OK)
async def get_pictures(picture_id: int,user: User = Depends(current_user),
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
        instances = results.scalars().first()
        with open(f"./temp/temporary.png","wb+") as buff:
            decoded = base64.standard_b64decode(instances.picture)
            buff.write(decoded)
            return FileResponse(buff.name,media_type="image/png")

    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))


#
# with Image.open(infile) as im:
#     im.thumbnail(size)
#     im.save(outfile, "JPEG")







