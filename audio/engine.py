import os
from pydub import AudioSegment
from data.settings import timestr, MEDIA_DIR, BASE_DIR


def get_new_file_name(filename: str):
    return '{}_{}.mp3'.format(os.path.splitext(filename)[0], timestr)


def get_location_old_file(filename: str):
    return os.path.join(MEDIA_DIR, f'wav_files/{filename}')


def get_location_new_file(filename: str):
    new_filename = get_new_file_name(filename=filename)
    return os.path.join(MEDIA_DIR, f'mp3_files/{new_filename}')


def save_audio(
        file_path: str, save_file_path: str = BASE_DIR, format: str = 'mp3'
):
    AudioSegment.from_file(file_path).export(save_file_path, format=format)