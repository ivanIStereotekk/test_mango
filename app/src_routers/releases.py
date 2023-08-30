import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from datetime import datetime as dt
from app.models import User, Release
from app.schemas import ReleaseCreate
from app.users import fastapi_users
from app.db import get_async_session
from settings import root_dir

# Logger configuration
logging.basicConfig(filename=f'{root_dir}/logs/release_logger.log', encoding='utf-8', level=logging.INFO)

current_user = fastapi_users.current_user(active=True)

router = APIRouter(
    dependencies=[Depends(current_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/add",
             status_code=status.HTTP_201_CREATED)
async def add_release(release: ReleaseCreate,
                      session: AsyncSession = Depends(get_async_session)):
    """ Add release method"""
    now = dt.now()
    try:
        new_release = Release(name=release.name,
                              artist=release.artist,
                              genre=release.genre,
                              release_date=str(now),
                              story_text=release.story_text,
                              record_label=release.record_label,
                              filename=release.filename,
                              cover_id=release.cover_id)
        session.add(new_release)
        await session.commit()
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: >> {e} \n {add_release.__name__}")
        raise HTTPException(status_code=400, detail=str(e))
    logging.info(f"Added release >> {release.name}")
    return {"details": f"{status.HTTP_201_CREATED, release.name} Successfully added"}


@router.get("/get/{release_id}",
            status_code=status.HTTP_200_OK)
async def get_release_id(release_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    """
    Method to get release by id.
    :param user:
    :param session:
    :return:
    """
    try:
        statement = select(Release).where(Release.id == release_id)
        results = await session.execute(statement)
        instance = results.scalars().first()
        if instance:
            return instance
        else:
            return {"details": f"{status.HTTP_404_NOT_FOUND} NOT FOUND"}
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: >> {e} \n {get_release_id.__name__}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_by_name/",
            status_code=status.HTTP_200_OK)
async def get_release_name(release_name: str,
                           session: AsyncSession = Depends(get_async_session)):
    """
    Method to get release by name.
    :param release_name:
    :param user:
    :param session:
    :return:
    """
    try:
        statement = select(Release).where(Release.name == release_name)
        results = await session.execute(statement)
        instance = results.scalars().first()
        if instance:
            return instance
        else:
            return {"details": f"{status.HTTP_404_NOT_FOUND} NOT FOUND"}
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: >> {e} \n {get_release_name.__name__}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_all",
            status_code=status.HTTP_200_OK)
async def get_release_all(session: AsyncSession = Depends(get_async_session)):
    """
    Method to get all releases.
    :param session:
    :return:
    """
    try:
        statement = select(Release)
        results = await session.execute(statement)
        instances = results.scalars().all()
        if instances:
            return instances
        else:
            return {"details": f"{status.HTTP_404_NOT_FOUND} NOT FOUND"}
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: >> {e} \n {get_release_name.__name__}")
        raise HTTPException(status_code=400, detail=str(e))













@router.delete("/delete/{release_id}",
               status_code=status.HTTP_200_OK)
async def delete_release(release_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    """
    Method to find so delete release by id.
    :param release_id:
    :param user:
    :param session:
    :return:
    """
    try:
        statement = select(Release).where(Release.id == release_id)
        results = await session.execute(statement)
        instance = results.scalars().first()
        if instance:
            await session.delete(instance)
            await session.commit()
            return {"details": f"{status.HTTP_200_OK} Successfully deleted"}
        else:
            return {"details": f"{status.HTTP_404_NOT_FOUND} Not found"}

    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: >> {e} \n {delete_release.__name__}")
        raise HTTPException(status_code=400, detail=str(e))
