import yt_downloader.core as core
import yt_downloader.config as config
import logging
import argparse

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--single", help="Set download mode to single. Requires YouTube video link as an argument in quotation marks.")
    group.add_argument("-m", "--multiple", help="Set download mode to multiple. Reads YouTube video links from youtube_urls.txt.", action="store_true")
    args = parser.parse_args()
    if args.single:
        core.process_url(args.single)
        logging.info("Process finished.")
    elif args.multiple:
        with open(config.YT_URLS_FILE) as file:
            for url in file:
                core.process_url(url.strip())
        logging.info("Process finished.")
    else:
        parser.print_help()