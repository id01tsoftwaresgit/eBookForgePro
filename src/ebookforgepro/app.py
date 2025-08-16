import os
import sys
import json
import subprocess
import threading
import traceback
import datetime
import base64
from pathlib import Path

# GUI Toolkit
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as tb

# Local application imports
from .core import (
    APP_NAME, APP_VERSION, APP_ID, PROJECT_DIR, ASSETS, BUILD, ICO_PATH, EMBED_ICO, TRAINING_DATA,
    scaffold_from_meta, autonomous_generation, clean_text
)
from .ai import Expander
from .exporters import Exporter
from .uploaders import Uploader
from .music import MusicGenerator

class App(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry("1240x840")
        self.minsize(1080, 720)
        if ICO_PATH.exists():
            try:
                self.iconbitmap(ICO_PATH)
            except Exception: pass

        self.api_cfg = self._load_api_settings()
        self.first_text = ""
        self.music_generator = MusicGenerator()
        self._build_ui()

    def _load_api_settings(self):
        defaults = {
            "mode": "offline", "openai_api_key": "", "openai_model": "gpt-4o-mini",
            "openai_base": "https://api.openai.com/v1", "gemini_api_key": "", "gemini_model": "gemini-1.5-flash",
            "local_base": "http://127.0.0.1:11434", "local_model": "llama3", "llama_cpp_model_path": ""
        }
        settings_file = PROJECT_DIR / "api_settings.json"
        if settings_file.exists():
            try:
                with open(settings_file, "r") as f:
                    return {**defaults, **json.load(f)}
            except Exception as e:
                self.log(f"Could not load API settings: {e}")
        return defaults

    def _build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True)

        tabs = {
            "Metadata": ttk.Frame(nb), "Compose": ttk.Frame(nb), "Preview": ttk.Frame(nb),
            "Export": ttk.Frame(nb), "Upload": ttk.Frame(nb), "APIs": ttk.Frame(nb),
            "Music": ttk.Frame(nb), "Windows Build": ttk.Frame(nb), "Diagnostics": ttk.Frame(nb),
        }
        for name, frame in tabs.items():
            nb.add(frame, text=name)

        self._build_metadata_tab(tabs["Metadata"])
        self._build_compose_tab(tabs["Compose"])
        self._build_export_tab(tabs["Export"])
        self._build_api_tab(tabs["APIs"])
        self._build_music_tab(tabs["Music"])
        self._build_diagnostics_tab(tabs["Diagnostics"])

    def _build_metadata_tab(self, tab):
        # ... implementation ...
        pass

    def _build_compose_tab(self, tab):
        # ... implementation ...
        pass

    def _build_export_tab(self, tab):
        # ... implementation ...
        pass

    def _build_api_tab(self, tab):
        # ... implementation ...
        pass

    def _build_music_tab(self, tab):
        container = ttk.Frame(tab, padding=15)
        container.pack(fill=tk.BOTH, expand=True)
        self.music_prompt_var = tk.StringVar(value="An epic cinematic theme")
        self.music_duration_var = tk.IntVar(value=10)
        self.music_status_var = tk.StringVar(value="Ready.")

        ttk.Label(container, text="Prompt:").pack(anchor="w")
        ttk.Entry(container, textvariable=self.music_prompt_var).pack(fill=tk.X)
        ttk.Label(container, text="Duration (seconds):").pack(anchor="w")
        ttk.Scale(container, from_=5, to=30, variable=self.music_duration_var).pack(fill=tk.X)
        ttk.Button(container, text="Generate Music", command=self.do_music_generation).pack(pady=10)
        ttk.Label(container, textvariable=self.music_status_var).pack()

    def _build_diagnostics_tab(self, tab):
        self.diag_txt = tk.Text(tab, wrap="word")
        self.diag_txt.pack(fill=tk.BOTH, expand=True)

    def log(self, msg):
        self.diag_txt.configure(state="normal")
        self.diag_txt.insert("end", f"{datetime.datetime.now().strftime('%H:%M:%S')} - {msg}\n")
        self.diag_txt.see("end")
        self.diag_txt.configure(state="disabled")

    def do_music_generation(self):
        prompt = self.music_prompt_var.get()
        duration = self.music_duration_var.get()
        if not prompt:
            messagebox.showwarning("Input Required", "Please enter a music prompt.")
            return

        self.config(cursor="wait")
        self.update_idletasks()

        def task():
            try:
                self.log(f"Starting music generation...")
                self.music_status_var.set("Loading model and generating...")
                audio_values, sampling_rate = self.music_generator.generate(prompt, duration)
                filepath = self.music_generator.save_wav(audio_values, sampling_rate, prompt)
                self.log(f"Music generation complete: {filepath}")
                self.music_status_var.set(f"Success! Saved to: {filepath}")
            except Exception as e:
                self.log(f"Music generation failed: {e}")
                self.music_status_var.set(f"Error: {e}")
            finally:
                self.config(cursor="")

        threading.Thread(target=task, daemon=True).start()
