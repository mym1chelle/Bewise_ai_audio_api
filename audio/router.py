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
from fastapi import HTTPException
from fastapi import status
from users.models import UserManager
from audio.models import Record


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
        print(save_path)

        async with open(file_location, 'wb+') as f:
            await f.write(file.file.read())
        # with open(file_location, "wb+") as file_object:
        #     file_object.write(file.file.read())

        save_audio(
            file_path=file_location,
            save_file_path=save_path
        )
        print(user.uuid)
        audio = Record(
            filename=file.filename,
            path=save_path,
            user_uuid=user.uuid
        )
        session.add(audio)
        await session.commit()

        return {'link': f'http://localhost:8000/record?id={audio.uuid}&user={user.uuid}'}


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
        print('record.user_uuid', type(record.user_uuid))
        print('user', type(user))
        print('record.path', record.path)
        new_filename = get_new_file_name(filename=record.filename)
        print('new_filename', new_filename)
        if str(record.user_uuid) == user:
            new_filename = get_new_file_name(filename=record.filename)
            print('record.path', record.path)
            print('new_filename', new_filename)
            v = FileResponse(
                path=record.path,
                media_type='application/octet-stream',
                filename='new_filename.mp3'
            )
            print('File', v)
            return v
    else:
        return 'ошибка'
