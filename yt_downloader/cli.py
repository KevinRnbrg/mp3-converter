import yt_downloader.core as core
import yt_downloader.config as config
import yt_downloader.exceptions as exceptions
import logging
import argparse


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
    )
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--single", help="Set download mode to single. Requires YouTube video link as an argument in quotation marks.")
    group.add_argument("-m", "--multiple", help="Set download mode to multiple. Reads YouTube video links from youtube_urls.txt.", action="store_true")
    args = parser.parse_args()
    if args.single:
        process_single_url(args.single)
        _log_completion(single=True)
    elif args.multiple:
        process_multiple_urls(config.YT_URLS_FILE)
        _log_completion(single=False)
    else:
        parser.print_help()


def _log_completion(*, single: bool) -> None:
    if single:
        logging.info("Process finished.")
    else:
        logging.info("All processes finished.")


def process_single_url(url: str) -> None:
    try:
        core.process_url(url.strip())
    except exceptions.YtDownloaderError as e:
        logging.error(e)


def process_multiple_urls(file_path: str) -> None:
    try:
        with open(file_path, encoding="utf-8") as file:
            for url in file:
                url = url.strip()
                if url:
                    process_single_url(url)
    except FileNotFoundError:
        logging.error("URLs file not found: %s", file_path)