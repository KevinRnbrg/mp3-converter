from slugify import slugify
import yt_downloader.config as config
import logging
import os

def remove_video_file(video_file):
    try:
        if os.path.exists(video_file) and video_file is not None:
            os.remove(video_file)
    except (FileNotFoundError, PermissionError, OSError):
        logging.error("Temporary file removal failed.")

def get_formatted_title(title: str):
    slugified = slugify(
        title, 
        max_length=config.TITLE_MAX_LENGTH,
        separator="_", 
        lowercase=False
    )
    return slugified