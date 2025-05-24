# Don't save mp4 file to pc, only mp3
# create new folder to desktop with mp3 files inside
# can add many links, will show converting progress

import os
from moviepy.editor import *

def download_MP4_from_YT(link):
    print("Downloading MP4 from YouTube")
    mp4_file = print("logic to find mp4 file from yt")
    return mp4_file

def convert_MP4_to_MP3(file_name): # surround with try?
    print("Converting mp4 to mp3")
    video = VideoFileClip(f"{file_name}.mp4")
    video.audio.write_audiofile(f"{file_name}.mp3")

def main():
    print("Start application")
    yt_link = input("Paste YouTube link:")
    mp4_file = download_MP4_from_YT(yt_link)
    # convert_MP4_to_MP3(mp4_file)
    dir_name = "mp3_files"
    try:
        os.mkdir(dir_name)
        print(f'Directory {dir_name} created successfully.')
        # add mp3 files inside
    except FileExistsError:
        print(f"Directory '{dir_name}' already exists.") # add fiels inside
    except PermissionError:
        print(f"Permission denied: Unable to create '{dir_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    print("Converting done") # + add filepath to show where files are

main()