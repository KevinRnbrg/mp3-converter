# Everything is globally scoped. No separation between CLI interface, business logic, and I/O. Refactor into at least 3 layers: CLI interface (parsing, I/O), Core logic (convert/download/etc.), Helpers/utilities
# Not testable. No unit-testable functions, no logging, no modularity.
# No real logging. No visibility into failures or skipped items. Add logging with levels (info, warning, error) instead of print.
# Allow running headless (e.g., through command line args, not only input()). Ex: 'main.py -single "https://www.youtube.com/video"', "main.py -multiple C:\Path\to\file"
# Hardcoded constants (like filename, dir names) instead of config.

import os
from pytubefix import YouTube
import pytubefix.exceptions as exceptions
from moviepy import AudioFileClip
from urllib.parse import urlparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s' # colored logs for readability?
)

dir_name = "audio"
yt_urls_file = "youtube_urls.txt"
title_max_length = 56

def process_user_input(url):
    yt = create_youtube_object(url)
    if yt is not None:
        download_MP3_file(yt)
        logging.info("Audio file downloaded.") # For looping downloads logs too much clutter. MoviePy already logs success.
    else:
        logging.warning("Skipping download for invalid or unavailable video: %s", url)

def create_youtube_object(url):
    try:
        validate_url(url)
        yt = YouTube(url)
        return yt
    except exceptions.RegexMatchError:
        logging.error("URL format in invalid: %s", url)
    except exceptions.VideoUnavailable:
        logging.error("Video is unavailable: %s", url)
    except Exception as e:
        logging.error("Error occured while creating YouTube object: %s", e)
    return None

def download_MP3_file(yt):
    video_file = get_highest_bitrate_video_from_YT(yt)
    try:
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        write_audio_file_from_video(video_file, yt)
    except Exception as e:
        remove_video_file(video_file)
        logging.error("Error during audio file writing: %s", e) # needs better handling
    finally:
        remove_video_file(video_file)

def validate_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https":
        raise Exception("Invalid scheme for URL: %s", url)
    if parsed_url.netloc not in ("www.youtube.com", "youtu.be"):
        raise Exception("Invalid domain name for URL: %s", url)
    if parsed_url.path != "/watch":
        raise Exception("Invalid path for URL: %s", url) # ('Invalid path for URL: %s', 'https:/...') - looks ugly. Fixable?

def get_highest_bitrate_video_from_YT(yt_object):
    try:
        audio_streams = yt_object.streams.filter(only_audio=True)
        stream = max(audio_streams, key=lambda s: int(s.abr.replace('kbps', '')))
        if not stream:
            raise Exception("No streams found for video.")
        else:
            return stream.download(filename='temp_audio.mp4')
    except Exception as e:
        logging.error("Error during finding stream: %s", e)

def write_audio_file_from_video(video_file, yt_object):
    title = get_formatted_title(yt_object)
    mp3_file = title + ".mp3"
    output_mp3_path = os.path.join(dir_name, mp3_file)
    with AudioFileClip(video_file) as audio:
        audio = AudioFileClip(video_file)
        audio.write_audiofile(output_mp3_path)
        audio.close()

def remove_video_file(video_file):
    try:
        if os.path.exists(video_file) and video_file is not None:
            os.remove(video_file)
    except (FileNotFoundError, PermissionError, OSError):
        logging.error("Temporary file removal failed.")

def get_formatted_title(ytObject):
    # doesn't sanitize against invalid characters, truncation to title_max_length and just replacing is simplistic slugging and could lead to duplicates (add counter?)
    # use slugify or something similar
    video_title = ytObject.title
    short_title = video_title[:title_max_length].strip()
    return short_title.replace(" ", "_")

if __name__ == "__main__":
    # User input needs validation (ex: non-integer will crash).
    option = int(input("Write 1 for single and 2 for multiple URLs: "))
    if (option == 1):
        url = input("Paste YouTube link: ")
        process_user_input(url)
    elif (option == 2):
        with open(yt_urls_file) as file:
            for url in file:
                process_user_input(url)
        logging.info("Process finished.")
    else:
        logging.info("Unknown command.")