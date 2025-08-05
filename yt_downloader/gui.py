import core as core
import config as config
import logging
import re
import winsound
import tkinter as tk
from tkinter import Button
from tkinterdnd2 import DND_TEXT, TkinterDnD


class GUI(TkinterDnD.Tk):
    def __init__(self, title, window_size):
        super().__init__()
        self.title(title)
        self.geometry(window_size)
        self.entries = []  # Stores all entry frames
        self.create_widgets()

    def create_widgets(self):
        # --- Manual Entry Field ---
        entry_frame = tk.Frame(self)
        entry_frame.pack(padx=20, pady=(65, 0), fill='x')

        self.manual_entry = tk.Entry(entry_frame)
        self.manual_entry.pack(side='left', fill='x', expand=True)

        add_button = tk.Button(entry_frame, text="Add",
                               command=lambda: self.add_entry(self.manual_entry.get()))
        add_button.pack(side='left', padx=(5, 0))

        # --- Entry Container Frame (Drop Target) ---
        self.entry_container = tk.Frame(self)
        self.entry_container.pack(padx=20, pady=20, fill='both', expand=True)

        self.entry_container.drop_target_register(DND_TEXT)
        self.entry_container.dnd_bind('<<Drop>>', self.on_drop)

        # --- Action Buttons ---
        self.process_urls_btn = Button(
            self, text="Process URLs", command=self.process_urls)
        self.process_urls_btn.pack(pady=10)

        self.quit_btn = Button(self, text="Quit", command=self.quit)
        self.quit_btn.pack(pady=10)

    def add_entry(self, url):
        url = url.strip()

        # Validate YouTube URL format
        if not re.match(r'https?://(www\.)?(youtube\.com|youtu\.be)/', url):
            self.show_notification("Invalid YouTube URL.")
            return

        # Create and pack entry frame
        item_frame = tk.Frame(self.entry_container)
        item_frame.pack(fill='x', pady=2)

        label = tk.Label(item_frame, text=url, anchor='w')
        label.pack(side='left', fill='x', expand=True)

        delete_btn = tk.Button(item_frame, text="❌",
                               command=lambda: self.delete_entry(item_frame))
        delete_btn.pack(side='right')

        self.entries.append(item_frame)

        # Feedback
        winsound.PlaySound("yt_downloader/assets/drop.wav",
                           winsound.SND_FILENAME | winsound.SND_ASYNC)
        self.show_notification("YouTube URL added.")

    def delete_entry(self, item_frame):
        item_frame.destroy()
        if item_frame in self.entries:
            self.entries.remove(item_frame)

    def on_drop(self, event):
        data = event.data.strip()
        print("Dropped data:", repr(data))
        self.add_entry(data)

    def process_urls(self):
        for entry in self.entries:
            label = entry.winfo_children()[0]  # First child is the Label
            url = label.cget("text").strip()
            self.process_single_url(url)

    def process_single_url(self, url):
        try:
            core.process_url(url)
        except Exception as e:
            logging.error(e)
        logging.info("Process finished.")

    def show_notification(self, message, duration=3000):
        notif = tk.Toplevel(self)
        notif.overrideredirect(True)
        notif.attributes("-topmost", True)
        notif.attributes("-alpha", 0.0)  # Start fully transparent

        # Notification size
        width = 250
        height = 50

        # Place near bottom-left of main window
        self.update_idletasks()  # Ensure geometry is up to date
        x = self.winfo_x() + (self.winfo_width() - width) // 2
        y = self.winfo_y() + 40
        notif.geometry(f"{width}x{height}+{x}+{y}")

        label = tk.Label(
            notif,
            text=message,
            bg="#5FE8FA",
            fg="black",
            font=("Segoe UI", 10),
            padx=10,
            pady=10
        )
        label.pack(fill='both', expand=True)

        # Fade in
        self._fade_in(notif, target_alpha=0.95, step=0.05)

        # After duration, fade out
        notif.after(duration, lambda: self._fade_out(notif, step=0.05))

    def _fade_in(self, window, target_alpha=1.0, step=0.05):
        alpha = window.attributes("-alpha")
        if alpha < target_alpha:
            alpha = min(alpha + step, target_alpha)
            window.attributes("-alpha", alpha)
            window.after(30, lambda: self._fade_in(window, target_alpha, step))

    def _fade_out(self, window, step=0.05):
        alpha = window.attributes("-alpha")
        if alpha > 0:
            alpha = max(alpha - step, 0)
            window.attributes("-alpha", alpha)
            window.after(30, lambda: self._fade_out(window, step))
        else:
            window.destroy()


UI = GUI("MP3 Downloader", "500x500")
UI.mainloop()
