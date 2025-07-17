from setuptools import setup, find_packages

requirements = []
with open("requirements.txt", "r") as file:
    for requirement in file:
        if requirement.strip() and not requirement.startswith("#") and not requirement.startswith("//"):
            requirements.append(requirement)

setup(
    name="yt_downloader",
    version="0.1",
    packages=find_packages(),
    install_requires=[
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
    ],
    entry_points={
        "console_scripts": [
            "yt_downloader=yt_downloader.cli:main"
        ]
    },
)