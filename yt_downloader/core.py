import os
from pytubefix import YouTube
from moviepy import AudioFileClip
from urllib.parse import urlparse
import yt_downloader.utils as utils
import yt_downloader.config as config
from yt_downloader.exceptions import InvalidURLError, DownloadError

# For testing assert correct exception rise and are catched and for correct inputs assert nothing goes wrong
# Everything needs mocking except validate_url in unit tests

def process_url(url: str) -> None:
    yt = create_youtube_object(url)
    if yt is None:
        raise DownloadError("Invalid or unavailable video")
    video_file = download_highest_bitrate_video(yt)
    if video_file is None:
        raise DownloadError("Could not find video to process")
    create_mp3_file(video_file, yt.title)

def create_youtube_object(url: str) -> YouTube:
    validate_url(url)
    return YouTube(url)

def validate_url(url: str) -> None:
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https":
        raise InvalidURLError(f"Invalid scheme for URL: {url}")
    if parsed_url.netloc not in ("www.youtube.com", "youtu.be"):
        raise InvalidURLError(f"Invalid domain name for URL: {url}")
    if parsed_url.netloc == "www.youtube.com":
        if parsed_url.path not in ("/watch", "/shorts"):
            raise InvalidURLError(f"Invalid path for URL: {url}")

def download_highest_bitrate_video(yt_object: YouTube, temp_file: str = 'temp_video.mp4') -> str:
    audio_streams = yt_object.streams.filter(only_audio=True)
    if not audio_streams:
        raise DownloadError("No audio streams found for video.")
    stream = max(audio_streams, key=lambda s: int(s.abr.replace('kbps', '')))
    if not stream:
        raise DownloadError("No streams found for video.")
    return stream.download(filename=temp_file)

def create_mp3_file(video_file: str, title: str) -> None:
    try:
        if not os.path.exists(config.AUDIO_DIR):
            os.mkdir(config.AUDIO_DIR)
        write_audio_file_from_video(video_file, title)
    finally:
        utils.remove_video_file(video_file)

def write_audio_file_from_video(video_file: str, title: str) -> None:
    title = utils.get_formatted_title(title)
    mp3_file = title + ".mp3"
    output_mp3_path = os.path.join(config.AUDIO_DIR, mp3_file)
    with AudioFileClip(video_file) as audio:
        audio.write_audiofile(output_mp3_path)