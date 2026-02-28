from slugify import slugify
import yt_downloader.config as config
import os

# Write tests

def remove_video_file(video_file: str | None) -> None:
    try:
        if video_file is not None and os.path.exists(video_file):
            os.remove(video_file)
    except (FileNotFoundError, PermissionError, OSError):
        raise

def get_formatted_title(title: str) -> str:
    slugified = slugify(
        title, 
        max_length=config.TITLE_MAX_LENGTH,
        separator="_", 
        lowercase=False
    )
    return slugified