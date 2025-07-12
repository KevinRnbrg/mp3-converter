import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "audio")
YT_URLS_FILE = os.path.join(PROJECT_ROOT, "youtube_urls.txt")
TITLE_MAX_LENGTH = 60