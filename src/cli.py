# Allow downloading MP3s from YouTube playlists

from core import process_user_input
import logging
import config
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--single", help="Set download mode to single. Requires YouTube video link as an argument in quotation marks.")
    group.add_argument("-m", "--multiple", help="Set download mode to multiple. Reads YouTube video links from youtube_urls.txt.", action="store_true") # for future: Requires path to a .txt file that contains YouTube links separated on individual lines.
    args = parser.parse_args()
    if args.single:
        process_user_input(args.single)
        logging.info("Process finished.")
    elif args.multiple:
        with open(config.YT_URLS_FILE) as file:
            for url in file:
                process_user_input(url.strip())
        logging.info("Process finished.")
    else:
        parser.print_help()