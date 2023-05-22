from aiofiles import open
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from data.db import get_async_session
from audio.engine import (
    get_new_file_name,
    get_location_old_file,
    save_audio,
    get_location_new_file
)
from sqlalchemy.exc import DBAPIError
from fastapi import HTTPException, status
from users.models import UserManager
from audio.models import Record
from audio.schemas import SendLinkModel
from data.settings import get_link


router = APIRouter(
    prefix='/record',
    tags=['Records']
)


@router.post('/uploadfile/')
async def upload_file(
    file: UploadFile,
    token: str,
    uuid: str,
    session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        user_manager = UserManager(session)
    user = await user_manager.get_current_user(
        token=token,
        uuid=uuid
    )
    if user:
        file_location = get_location_old_file(filename=file.filename)
        save_path = get_location_new_file(filename=file.filename)

        async with open(file_location, 'wb+') as f:
            await f.write(file.file.read())

        save_audio(
            file_path=file_location,
            save_file_path=save_path
        )
        audio = Record(
            filename=file.filename,
            path=save_path,
            user_uuid=user.uuid
        )
        session.add(audio)
        await session.commit()

        return SendLinkModel(
            link=get_link(
                audio_uuid=audio.uuid,
                user_uuid=user.uuid
            )
        )


@router.get('/')
async def dowload_file(
    id: str,
    user: str,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Record).where(Record.uuid == id)
        result = await session.execute(query)
    except DBAPIError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Link error',
        )
    record = result.scalars().first()
    if record:
        new_filename = get_new_file_name(filename=record.filename)
        if str(record.user_uuid) == user:
            new_filename = get_new_file_name(filename=record.filename)
            return FileResponse(
                path=record.path,
                media_type='application/octet-stream',
                filename=new_filename
            )
    else:
        return 'ошибка'
