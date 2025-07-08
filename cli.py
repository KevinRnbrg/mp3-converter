from core import process_user_input
import logging
import config

if __name__ == "__main__":
    # User input needs validation (ex: non-integer will crash).
    option = int(input("Write 1 for single and 2 for multiple URLs: "))
    if (option == 1):
        url = input("Paste YouTube link: ")
        process_user_input(url)
    elif (option == 2):
        with open(config.YT_URLS_FILE) as file:
            for url in file:
                process_user_input(url.strip())
        logging.info("Process finished.")
    else:
        logging.info("Unknown command.")