import os
from pytubefix import YouTube
from moviepy import *

dir_name = "audio"
yt_urls_file = "youtube_urls.txt"

def downloadMP3File(yt_url):
    ytObject = YouTube(yt_url)
    video_file = getVideoFileFromURL(ytObject)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    writeAudioFileFromVideo(video_file, ytObject)
    if os.path.exists(video_file):
        os.remove(video_file)

def getVideoFileFromURL(ytObject):
    stream = ytObject.streams.filter(only_audio=True).first()
    return stream.download(filename='temp_audio.mp4')

def writeAudioFileFromVideo(video_file, ytObject):
    title = getFormattedTitle(ytObject)
    mp3_file = title + ".mp3"
    output_mp3_path = os.path.join(dir_name, mp3_file)
    audio = AudioFileClip(video_file)
    audio.write_audiofile(output_mp3_path)
    audio.close()

def getFormattedTitle(ytObject):
    video_title = ytObject.title
    short_title = video_title[:56].strip()
    return short_title.replace(" ", "_")

def main():
    option = int(input("Write 1 for single and 2 for multiple URLs: "))
    if (option == 1):
        yt_url = input("Paste YouTube link: ")
        downloadMP3File(yt_url)
        print("Audio file downloaded.")
    elif (option == 2):
        with open(yt_urls_file) as file:
            for url in file:
                downloadMP3File(url)
        # optimize logic?
        print("Audio files downloaded.")
    else:
        print("Unknown command.")

main()