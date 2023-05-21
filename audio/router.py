import os
from aiofiles import open
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from data.db import get_async_session
from data.settings import timestr, BASE_DIR, MEDIA_DIR
from audio.models import Record
from audio.engine import (
    get_new_file_name,
    get_location_old_file,
    save_audio,
    get_location_new_file
)


router = APIRouter(
    prefix='/record',
    tags=['Records']
)


@router.post('/uploadfile/')
async def upload_file(
    file: UploadFile,
    session: AsyncSession = Depends(get_async_session)
):
    new_filename = get_new_file_name(filename=file.filename)
    file_location = get_location_old_file(filename=file.filename)
    save_path = get_location_new_file(filename=file.filename)

    async with open(file_location, 'wb+') as f:
        await f.write(file.file.read())
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(file.file.read())

    save_audio(
        file_path=file_location,
        save_file_path=save_path
    )
    # data = await file.read()
    # audio = AudioRecording(
    #     name=file.filename,
    #     data=await file.read()
    # )
    # session.add(audio)
    # await session.commit()
    # return FileResponse(
    #     path=SAVE_FILE_PATH,
    #     media_type='application/octet-stream',
    #     filename=new_filename
    # )

@router.post('/download/{audio_id}')
async def dowload_file(
    audio_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(AudioRecording).where(
        AudioRecording.uuid == audio_id
    )
    file = (await session.execute(query)).scalars().first()
    
    
    