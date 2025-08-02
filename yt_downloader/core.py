import os
from pytubefix import YouTube
from moviepy import AudioFileClip
from urllib.parse import urlparse
import yt_downloader.utils as utils
import yt_downloader.config as config
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

# For testing assert correct exception rise and are catched and for correct inputs assert nothing goes wrong
# Everything needs mocking except validate_url in unit tests

def process_url(url: str, isVideo: bool): # to test this orchestration function mock all methods called to test different paths (success, exceptions)
    yt = create_youtube_object(url)
    if yt is None:
        raise ValueError("Invalid or unavailable video.")
    if isVideo:
        video_file = download_highest_bitrate_video(yt)
    else:
        video_file = download_highest_bitrate_audio(yt)
        create_mp3_file(video_file, yt.title)

def create_youtube_object(url: str) -> YouTube:
    validate_url(url)
    return YouTube(url)

def validate_url(url: str):
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https":
        raise ValueError(f"Invalid scheme for URL: {url}")
    if parsed_url.netloc not in ("www.youtube.com", "youtu.be"):
        raise ValueError(f"Invalid domain name for URL: {url}")
    if parsed_url.netloc == "www.youtube.com":
        if parsed_url.path not in ("/watch", "/shorts"):
            raise ValueError(f"Invalid path for URL: {url}")

def download_highest_bitrate_audio(yt_object: YouTube, temp_file: str = 'temp_video.mp4'): # Mock yt.object.streams.filter and stream.download methods for testing
    audio_streams = yt_object.streams.filter(only_audio=True)
    if not audio_streams:
        raise RuntimeError("No audio streams found for video.")
    max_quality_stream = max(audio_streams, key=lambda s: int(s.abr.replace('kbps', '')))
    if not max_quality_stream:
        raise RuntimeError("No streams found for video.")
    video_file = max_quality_stream.download(filename=temp_file)
    if video_file is None:
        raise RuntimeError("Could not find video to process")
    return video_file

def download_highest_bitrate_video(yt_object: YouTube):
    video_streams = yt_object.streams.filter(progressive=True)
    if not video_streams:
        raise RuntimeError("No video streams found for video.")
    max_quality_stream = max(video_streams, key=lambda s: int(s.resolution.replace('p', '')))
    if not max_quality_stream:
        raise RuntimeError("No streams found for video.")
    video_title = yt_object.title + ".mp4"
    video_path = mp4_path()
    video_file = max_quality_stream.download(video_path, filename=video_title)
    if video_file is None:
        raise RuntimeError("Could not find video to process")
    return video_file

def create_mp3_file(video_file, title): # mock file system operations and write_audio_file_from_video (creates the dir, calls writer, always removes video file)
    if not os.path.exists(config.AUDIO_DIR):
        os.mkdir(config.AUDIO_DIR)
    write_audio_file_from_video(video_file, title)

def write_audio_file_from_video(video_file, title: str): # Mock AudioFileClip and file system. Assert call for audio.write_audiofile with the correct path.
    title = utils.get_formatted_title(title)
    mp3_file = title + ".mp3"
    output_mp3_path = os.path.join(config.AUDIO_DIR, mp3_file)
    try:
        with AudioFileClip(video_file) as audio:
            audio.write_audiofile(output_mp3_path)
    finally:
        utils.remove_video_file(video_file)

def mp4_path():
    if not os.path.exists(config.VIDEO_DIR):
        os.mkdir(config.VIDEO_DIR)
    return config.VIDEO_DIR