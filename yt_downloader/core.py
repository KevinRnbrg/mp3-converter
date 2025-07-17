import os
from pytubefix import YouTube
import pytubefix.exceptions as exceptions
from moviepy import AudioFileClip
from urllib.parse import urlparse
import yt_downloader.utils as utils
import yt_downloader.config as config
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

def process_url(url: str):
    yt = create_youtube_object(url)
    if yt is not None:
        video_file = download_highest_bitrate_video(yt)
        if video_file is not None:
            create_mp3_file(video_file, yt.title)
            logging.info("Audio file downloaded.")
        else:
            logging.error("Could not find video to process.")
    else:
        logging.warning("Skipping download for invalid or unavailable video: %s", url)

def create_mp3_file(video_file, title):
    try:
        if not os.path.exists(config.AUDIO_DIR):
            os.mkdir(config.AUDIO_DIR)
        write_audio_file_from_video(video_file, title)
    except Exception as e:
        utils.remove_video_file(video_file)
        logging.error("Error during audio file writing: %s", e)
    finally:
        utils.remove_video_file(video_file)

def create_youtube_object(url: str) -> YouTube | None:
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

def validate_url(url: str):
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https":
        raise Exception(f"Invalid scheme for URL: {url}")
    if parsed_url.netloc not in ("www.youtube.com", "youtu.be"):
        raise Exception(f"Invalid domain name for URL: {url}")
    if parsed_url.netloc == "www.youtube.com":
        if parsed_url.path not in ("/watch", "/shorts"):
            raise Exception(f"Invalid path for URL: {url}")

def download_highest_bitrate_video(yt_object: YouTube):
    try:
        audio_streams = yt_object.streams.filter(only_audio=True)
        stream = max(audio_streams, key=lambda s: int(s.abr.replace('kbps', '')))
        if not stream:
            raise Exception("No streams found for video.")
        else:
            return stream.download(filename='temp_video.mp4')
    except Exception as e:
        logging.error("Error during finding stream: %s", e)
    return None

def write_audio_file_from_video(video_file, title: str):
    title = utils.get_formatted_title(title)
    mp3_file = title + ".mp3"
    output_mp3_path = os.path.join(config.AUDIO_DIR, mp3_file)
    with AudioFileClip(video_file) as audio:
        audio.write_audiofile(output_mp3_path)