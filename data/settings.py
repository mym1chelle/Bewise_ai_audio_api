import time
import os
from pathlib import Path
from data.config import load_config


config = load_config(".env")
timestr = time.strftime('%Y%m%d-%H%M%S')
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = os.path.join(BASE_DIR, 'audio_recordings')
HOST = config.link.host


def get_link(audio_uuid: str, user_uuid: str):
    return f'http://{HOST}:8000/record?id={audio_uuid}&user={user_uuid}'
