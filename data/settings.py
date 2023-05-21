import time
import os
from pathlib import Path


timestr = time.strftime('%Y%m%d-%H%M%S')
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = os.path.join(BASE_DIR, 'audio_recordings')
