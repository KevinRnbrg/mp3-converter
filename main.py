# Everything is globally scoped. No separation between CLI interface, business logic, and I/O. Refactor into at least 3 layers: CLI interface (parsing, I/O), Core logic (convert/download/etc.), Helpers/utilities
# Not testable. No unit-testable functions, no logging, no modularity.
# No real logging. No visibility into failures or skipped items. Add logging with levels (info, warning, error) instead of print.
# Allow running headless (e.g., through command line args, not only input()). Ex: 'main.py -single "https://www.youtube.com/video"', "main.py -multiple C:\Path\to\file"
# Hardcoded constants (like filename, dir names) instead of config.

import os
from pytubefix import YouTube
from moviepy import AudioFileClip
from urllib.parse import urlparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

dir_name = "audio"
yt_urls_file = "youtube_urls.txt"
title_max_length = 56

def download_MP3_file(yt_url):
    yt_object = YouTube(yt_url) # is successful? Validate URL first and check if create YouTube() works.
    video_file = get_highest_bitrate_video_from_YT(yt_object)
    try:
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        write_audio_file_from_video(video_file, yt_object)
    except Exception as e:
        os.remove(video_file)
        logging.error("Error during audio file writing: ", e) # needs better handling
    finally:
        if os.path.exists(video_file):
            os.remove(video_file)

def get_highest_bitrate_video_from_YT(yt_object):
    try:
        audio_streams = yt_object.streams.filter(only_audio=True)
        stream = max(audio_streams, key=lambda s: int(s.abr.replace('kbps', '')))
        if not stream:
            raise Exception("No streams found for video.")
    except Exception as e:
        logging.error("Error during finding stream: " + e)
    return stream.download(filename='temp_audio.mp4')

def write_audio_file_from_video(video_file, yt_object):
    title = get_formatted_title(yt_object)
    mp3_file = title + ".mp3"
    output_mp3_path = os.path.join(dir_name, mp3_file)
    with AudioFileClip(video_file) as audio:
        audio = AudioFileClip(video_file)
        audio.write_audiofile(output_mp3_path)
        audio.close()

def get_formatted_title(ytObject):
    # doesn't sanitize against invalid characters, truncation to title_max_length and just replacing is simplistic slugging and could lead to duplicates (add counter?)
    # use slugify or something similar
    video_title = ytObject.title
    short_title = video_title[:title_max_length].strip()
    return short_title.replace(" ", "_")

if __name__ == "__main__":
    # wrap user input parsing in it's own function - needs validation (ex: non-integer will crash)
    option = int(input("Write 1 for single and 2 for multiple URLs: "))
    if (option == 1):
        yt_url = input("Paste YouTube link: ") # validate URL (make reusable logic for single and multiple)
        download_MP3_file(urlparse(yt_url).geturl())
        logging.info("Audio file downloaded.")
    elif (option == 2):
        # Validate URLs.
        # Add exception handling per URL to skip and continue on error.
        # Print or log progress and issues with specific entries.
        with open(yt_urls_file) as file:
            for url in file:
                download_MP3_file(urlparse(url).geturl())
        # optimize logic?
        logging.info("Audio files downloaded.")
    else:
        logging.info("Unknown command.")