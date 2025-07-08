# Not testable. No unit-testable functions, no logging, no modularity.
# Allow running headless (e.g., through command line args, not only input()). Ex: 'main.py -single "https://www.youtube.com/video"', "main.py -multiple C:\Path\to\file"
# Hardcoded constants (like filename, dir names) instead of config.
# Group python files in another folder?

import os
from pytubefix import YouTube
import pytubefix.exceptions as exceptions
from moviepy import AudioFileClip
from urllib.parse import urlparse
import utils
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

dir_name = "audio"

def process_user_input(url):
    yt = create_youtube_object(url)
    if yt is not None:
        download_MP3_file(yt)
        logging.info("Audio file downloaded.")
    else:
        logging.warning("Skipping download for invalid or unavailable video: %s", url)

def download_MP3_file(yt):
    video_file = get_highest_bitrate_video_from_YT(yt)
    if video_file is not None:
        try:
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            write_audio_file_from_video(video_file, yt)
        except Exception as e:
            utils.remove_video_file(video_file)
            logging.error("Error during audio file writing: %s", e)
        finally:
            utils.remove_video_file(video_file)
    else:
        logging.error("Could not find video to process.")

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

def validate_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https":
        raise Exception(f"Invalid scheme for URL: {url}")
    if parsed_url.netloc not in ("www.youtube.com", "youtu.be"):
        raise Exception(f"Invalid domain name for URL: {url}")
    if parsed_url.path != "/watch": # Rigid. YouTube has more varied paths for videos. Add more paths or use regex?
        raise Exception(f"Invalid path for URL: {url}")

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
    return None

def write_audio_file_from_video(video_file, yt_object):
    title = utils.get_formatted_title(yt_object.title)
    mp3_file = title + ".mp3"
    output_mp3_path = os.path.join(dir_name, mp3_file)
    with AudioFileClip(video_file) as audio:
        audio = AudioFileClip(video_file)
        audio.write_audiofile(output_mp3_path)
        audio.close()