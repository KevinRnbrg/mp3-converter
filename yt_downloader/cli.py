import argparse
import logging

from .config import YT_URLS_FILE
from .core import process_url

# Write unit tests (file reading, looping, error handling). Use mocks if necessary.

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--single", help="Set download mode to single. Requires YouTube video link as an argument in quotation marks.")
    group.add_argument("-m", "--multiple", help="Set download mode to multiple. Reads YouTube video links from youtube_urls.txt.", action="store_true")
    args = parser.parse_args()
    if args.single:
        process_single_url(args.single)
    elif args.multiple:
        process_multiple_urls(YT_URLS_FILE)
        logging.info("Process finished.")
    else:
        parser.print_help()

def process_single_url(url):
    try:
        process_url(url.strip())
    except Exception as e:
        logging.error(e)
    logging.info("Process finished.")

def process_multiple_urls(file_path):
    with open(file_path) as file:
        for url in file:
            process_single_url(url)
    logging.info("All processes finished.")