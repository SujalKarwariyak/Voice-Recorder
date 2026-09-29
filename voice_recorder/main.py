"""Application entry point."""

import tkinter as tk

from .gui import VoiceRecorderApp
from .logger import setup_logging


def main():
    setup_logging()
    root = tk.Tk()
    VoiceRecorderApp(root)
    root.mainloop()
