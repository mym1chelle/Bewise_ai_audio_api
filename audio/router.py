from aiofiles import open
from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    status,
    HTTPException
)
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
from sqlalchemy import select
from data.db import get_async_session
from data.settings import get_link
from audio.engine import (
    get_new_file_name,
    get_location_old_file,
    save_audio,
    get_location_new_file,
    check_file_extention
)
from audio.models import Record
from audio.schemas import SendLinkModel
from users.models import UserManager


router = APIRouter(
    prefix='/record',
    tags=['Records']
)


@router.post('/uploadfile/')
async def upload_file(
    file: UploadFile,
    uuid: str,
    token: str,
    session: AsyncSession = Depends(get_async_session)
):
    """Загрузка аудиофайла"""
    correct_file = check_file_extention(file.filename)
    if correct_file:
        async with session.begin():
            user_manager = UserManager(session)
        user = await user_manager.get_current_user(
            token=token,
            uuid=uuid
        )
        if user:
            file_location = get_location_old_file(filename=file.filename)
            save_path = get_location_new_file(filename=file.filename)
            new_filename = get_new_file_name(filename=file.filename)

            async with open(file_location, 'wb+') as f:
                await f.write(file.file.read())

            save_audio(
                file_path=file_location,
                save_file_path=save_path
            )
            audio = Record(
                filename=new_filename,
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
    """Скачивание сконвертированного аудиофайла"""
    incorrect_link = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail='Incorrect link',
    )
    try:
        query = select(Record).where(Record.uuid == id)
        result = await session.execute(query)
    except DBAPIError:
        raise incorrect_link
    record = result.scalars().first()
    if record:
        if str(record.user_uuid) == user:
            return FileResponse(
                path=record.path,
                media_type='application/octet-stream',
                filename=record.filename
            )
        else:
            raise incorrect_link
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found'
        )
