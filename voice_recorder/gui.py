"""Tkinter user interface (presentation layer only)."""

import logging
import queue
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from . import config, file_manager, validators
from .audio_recorder import AudioRecorder

log = logging.getLogger(__name__)


class VoiceRecorderApp:
    def __init__(self, root, recorder=None):
        self.root = root
        self.recorder = recorder or AudioRecorder()
        self.path = None
        self.duration = None
        root.title(config.APP_TITLE)
        root.geometry("520x560")
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", self.close)
        self._build()
        self._poll()

    def _build(self):
        f = ttk.Frame(self.root, padding=20)
        f.pack(fill=tk.BOTH, expand=True)
        self.unlimited = tk.BooleanVar()
        ttk.Checkbutton(f, text="Record until I click Stop", variable=self.unlimited,
                        command=self._toggle).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.duration_var = tk.StringVar(value=str(config.DEFAULT_DURATION_SECONDS))
        self.rate_var = tk.StringVar(value=str(config.DEFAULT_SAMPLE_RATE))
        self.channels_var = tk.StringVar(value="1 (Mono)")
        self.filename_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.spin = ttk.Spinbox(f, from_=config.MIN_DURATION_SECONDS,
                                to=config.MAX_DURATION_SECONDS, textvariable=self.duration_var)
        rows = [
            ("Duration (s):", self.spin),
            ("Sample rate (Hz):", ttk.Combobox(f, textvariable=self.rate_var, state="readonly",
                                               values=[str(r) for r in config.SAMPLE_RATES])),
            ("Channels:", ttk.Combobox(f, textvariable=self.channels_var, state="readonly",
                                       values=list(config.CHANNEL_OPTIONS))),
            ("Filename:", ttk.Entry(f, textvariable=self.filename_var)),
        ]
        for i, (label, widget) in enumerate(rows, start=1):
            ttk.Label(f, text=label).grid(row=i, column=0, sticky=tk.W, pady=4)
            widget.grid(row=i, column=1, sticky=tk.EW, padx=8)
        ttk.Button(f, text="Browse", command=self._browse).grid(row=4, column=2)
        ttk.Label(f, textvariable=self.status_var).grid(row=5, column=0, columnspan=3, pady=8)
        self.bar = ttk.Progressbar(f, maximum=100)
        self.bar.grid(row=6, column=0, columnspan=3, sticky=tk.EW)
        box = ttk.Frame(f)
        box.grid(row=7, column=0, columnspan=3, pady=12)
        self.start_btn = ttk.Button(box, text="Start", command=self.start)
        self.stop_btn = ttk.Button(box, text="Stop", command=self.recorder.stop, state=tk.DISABLED)
        self.start_btn.pack(side=tk.LEFT, padx=4)
        self.stop_btn.pack(side=tk.LEFT, padx=4)
        ttk.Button(box, text="Exit", command=self.close).pack(side=tk.LEFT, padx=4)
        ttk.Label(f, text="Recent recordings").grid(row=8, column=0, columnspan=3, sticky=tk.W)
        self.history = tk.Listbox(f, height=6)
        self.history.grid(row=9, column=0, columnspan=3, sticky=tk.EW)
        self._refresh_history()

    def _toggle(self):
        self.spin.config(state=tk.DISABLED if self.unlimited.get() else tk.NORMAL)

    def _browse(self):
        name = filedialog.asksaveasfilename(defaultextension=".wav",
                                            filetypes=[("WAV files", "*.wav")])
        if name:
            self.filename_var.set(name)

    def _refresh_history(self):
        self.history.delete(0, tk.END)
        for r in file_manager.list_recordings():
            self.history.insert(tk.END, f"{r['name']}  ({r['seconds']:.1f}s, {r['size_mb']:.2f} MB)")

    def start(self):
        try:
            self.duration = None if self.unlimited.get() else validators.validate_duration(
                self.duration_var.get())
            rate = validators.validate_sample_rate(self.rate_var.get())
            channels = validators.validate_channels(self.channels_var.get())
            self.path = validators.resolve_filename(self.filename_var.get())
            file_manager.ensure_parent(self.path)
        except (validators.ValidationError, OSError) as exc:
            messagebox.showerror("Invalid input", str(exc))
            return
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("Recording...")
        self.bar.config(value=0)
        self.recorder.start(self.path, self.duration, rate, channels)

    def _poll(self):
        """Drain worker events on the Tk thread (the only place widgets change)."""
        try:
            while True:
                kind, payload = self.recorder.events.get_nowait()
                if kind == "progress":
                    self.status_var.set(f"Recording... {payload:.1f}s")
                    if self.duration:
                        self.bar.config(value=min(payload / self.duration * 100, 100))
                else:
                    self._finished(kind, payload)
        except queue.Empty:
            pass
        self.root.after(100, self._poll)

    def _finished(self, kind, payload):
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        if kind == "done":
            self.status_var.set(f"Saved {payload.name} ({file_manager.file_size_mb(payload):.2f} MB)")
            self._refresh_history()
        else:
            self.status_var.set("Recording failed")
            messagebox.showerror("Recording error", str(payload))

    def close(self):
        if self.recorder.is_recording:
            self.recorder.stop()  # let the worker save the audio first
            self.status_var.set("Saving before exit...")
            self.root.after(150, self.close)
            return
        self.root.destroy()
