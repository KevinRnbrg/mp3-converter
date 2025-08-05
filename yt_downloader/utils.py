from slugify import slugify
import config as config
import os

# Write tests


def remove_video_file(video_file):  # Mock os.path.exists, os.remove
    try:
        if os.path.exists(video_file) and video_file is not None:
            os.remove(video_file)
    except (FileNotFoundError, PermissionError, OSError) as e:
        raise e


def get_formatted_title(title: str):
    slugified = slugify(
        title,
        max_length=config.TITLE_MAX_LENGTH,
        separator="_",
        lowercase=False
    )
    return slugified
