import yt_downloader.core as core
import yt_downloader.config as config
import logging
import argparse

# Write unit tests (file reading, looping, error handling). Use mocks if necessary.

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    type_group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--single", help="Set download mode to single. Requires YouTube video link as an argument in quotation marks.")
    group.add_argument("-m", "--multiple", help="Set download mode to multiple. Reads YouTube video links from youtube_urls.txt.", action="store_true")
    type_group.add_argument("-v", "--video", help="Set file type to VIDEO", action="store_true")
    type_group.add_argument("-mu", "--music", help="Set file type to MUSIC", action="store_true")
    # subparser = parser.add_subparsers()
    # file_type = subparser.add_parser("type", help="Choose the file type")
    # file_type.add_argument("type", choices=("video", "music"), help="Set file download type to VIDEO or MUSIC.")
    args = parser.parse_args()
    if args.music:
        if args.single:
            process_single_url(args.single, False)
        elif args.multiple:
            process_multiple_urls(config.YT_URLS_FILE)
            logging.info("Process finished.")
        else:
            parser.print_help()
    elif args.video:
        if args.single:
            process_single_url(args.single, True)
        elif args.multiple:
            process_multiple_urls(config.YT_URLS_FILE)
            logging.info("Process finished.")
        else:
            parser.print_help()
    else:
        parser.print_help()


def process_single_url(url, bool):
    try:
        core.process_url(url.strip(), bool)
    except Exception as e:
        logging.error(e)
    logging.info("Process finished.")

def process_multiple_urls(file_path):
    with open(file_path) as file:
        for url in file:
            process_single_url(url)
    logging.info("All processes finished.")