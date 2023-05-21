import os
from pathlib import Path
import time
from pydub import AudioSegment
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from data.db import get_async_session
from audio.models import AudioRecording

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = os.path.join(BASE_DIR, 'audio_recordings')

router = APIRouter(
    prefix='/audio',
    tags=['Audio']
)


@router.post('/uploadfile/')
async def upload_file(
    file: UploadFile,
    session: AsyncSession = Depends(get_async_session)
):
    print(BASE_DIR)
    timestr = time.strftime('%Y%m%d-%H%M%S')
    new_filename = '{}_{}.mp3'.format(os.path.splitext(file.filename)[0], timestr)
    file_location = os.path.join(MEDIA_DIR, f'wav_files/{file.filename}')
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    audio = AudioSegment.from_file(file_location)
    SAVE_FILE_PATH = os.path.join(MEDIA_DIR, f'mp3_files/{new_filename}')
    audio.export(SAVE_FILE_PATH, format='mp3')
    # data = await file.read()
    # audio = AudioRecording(
    #     name=file.filename,
    #     data=await file.read()
    # )
    # session.add(audio)
    # await session.commit()
    return FileResponse(
        path=SAVE_FILE_PATH,
        media_type='application/octet-stream',
        filename=new_filename
    )

@router.post('/download/{audio_id}')
async def dowload_file(
    audio_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(AudioRecording).where(
        AudioRecording.uuid == audio_id
    )
    file = (await session.execute(query)).scalars().first()
    
    
    