from setuptools import setup, find_packages

NAME = 'yt_downloader'
DESCRIPTION = 'YouTube audio and video downloader.'
URL = 'https://github.com/KevinRnbrg/mp3-converter'
REQUIRES_PYTHON = '>=3.9.0'
VERSION = '0.1.0'

REQUIRED = [
    "colorama==0.4.6",
    "decorator==5.2.1",
    "imageio==2.37.0",
    "imageio-ffmpeg==0.6.0",
    "iniconfig==2.1.0",
    "moviepy==2.2.1",
    "numpy==2.2.6",
    "packaging==25.0",
    "pillow==11.2.1",
    "pluggy==1.6.0",
    "proglog==0.1.12",
    "Pygments==2.19.2",
    "python-dotenv==1.1.0",
    "python-slugify==8.0.4",
    "pytube==15.0.0",
    "pytubefix==9.1.2",
    "text-unidecode==1.3",
    "tqdm==4.67.1"
]

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=REQUIRED,
    entry_points={
        "console_scripts": [
            "yt_downloader=yt_downloader.cli:main"
        ]
    },
    license='MIT'
)