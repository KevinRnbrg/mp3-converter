import core as core
import config as config
import logging
from tkinterdnd2 import DND_TEXT, TkinterDnD
from tkinter import Tk, Listbox, SINGLE, Button
import tkinter as tk
import re
import winsound

class GUI(TkinterDnD.Tk):
    def __init__(self, title, window_size):
        super().__init__()
        self.title(title)
        self.geometry(window_size)
        self.create_widgets()


    def create_widgets(self):
        # Create a Listbox widget instead of a Label
        self.listbox = tk.Listbox(self, width=60, height=10)
        self.listbox.pack(padx=20, pady=20)

        # Register the Listbox as a drop target for text
        self.listbox.drop_target_register(DND_TEXT)
        self.listbox.dnd_bind('<<Drop>>', self.on_drop)


        self.process_urls_btn = Button(self, text="Process URLs", command=self.process_urls)
        self.process_urls_btn.pack(pady=10)

        self.quit_btn = Button(self, text="Quit", command=self.quit)
        self.quit_btn.pack(pady=10)
    
    def on_drop(self, event):
        data = event.data.strip()
        print("Dropped data:", repr(data))
        if re.match(r'https?://(www\.)?(youtube\.com|youtu\.be)/', data):
            self.listbox.insert(tk.END, data)
            winsound.PlaySound("yt_downloader/assets/drop.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            print("Dropped data is not a valid YouTube URL.")

    def process_urls(self):
        # Get all items in the listbox
        urls = self.listbox.get(0, tk.END)
        for url in urls:
            self.process_single_url(url)
            
    def process_single_url(self, url):
        try:
            core.process_url(url.strip())
        except Exception as e:
            logging.error(e)
        logging.info("Process finished.")

    def process_multiple_urls(self,file_path):
        with open(file_path) as file:
            for url in file:
                process_single_url(url)
        logging.info("All processes finished.")

UI = GUI("MP3 Downloader", "500x500")
UI.mainloop()

