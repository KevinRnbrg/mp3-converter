from core import process_user_input
import logging

yt_urls_file = "youtube_urls.txt"

if __name__ == "__main__":
    # User input needs validation (ex: non-integer will crash).
    option = int(input("Write 1 for single and 2 for multiple URLs: "))
    if (option == 1):
        url = input("Paste YouTube link: ")
        process_user_input(url)
    elif (option == 2):
        with open(yt_urls_file) as file:
            for url in file:
                process_user_input(url)
        logging.info("Process finished.")
    else:
        logging.info("Unknown command.")