import os
from pytubefix import YouTube
from moviepy import *

dir_name = "audio"

def getVideoFileFromURL(yt_url):
    yt = YouTube(yt_url)
    stream = yt.streams.filter(only_audio=True).first()
    return stream.download(filename='temp_audio.mp4')

def writeAudioFileFromVideo(download_path):
    output_mp3_path = os.path.join(dir_name, "output.mp3")
    audio = AudioFileClip(download_path)
    audio.write_audiofile(output_mp3_path)
    audio.close()

def main():
    yt_url = input("Paste YouTube link: ")
    video_file = getVideoFileFromURL(yt_url)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    writeAudioFileFromVideo(video_file)
    if os.path.exists(video_file):
        os.remove(video_file)
    print("Audio file saved.")

main()