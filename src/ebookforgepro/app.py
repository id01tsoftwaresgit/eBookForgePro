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
from PIL import ImageTk, Image

# Local application imports
from .core import (
    APP_NAME, APP_VERSION, APP_ID, PROJECT_DIR, ASSETS, BUILD, ICO_PATH, EMBED_ICO, TRAINING_DATA,
    scaffold_from_meta, autonomous_generation, clean_text
)
from .ai import Expander
from .exporters import Exporter
from .uploaders import Uploader
from .music import MusicGenerator
from .image import ImageGenerator

class WinHelpers:
    @staticmethod
    def write_all():
        BUILD.mkdir(parents=True, exist_ok=True)
        ASSETS.mkdir(parents=True, exist_ok=True)
        if not ICO_PATH.exists():
            try:
                ICO_PATH.write_bytes(base64.b64decode(EMBED_ICO))
            except Exception: pass

        manifest = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity version="{APP_VERSION}.0" processorArchitecture="*" name="{APP_ID}" type="win32"/>
  <description>{APP_NAME}</description>
</assembly>'''.strip()
        (BUILD / "app.manifest").write_text(manifest, encoding="utf-8")

        script_path = "ebookforgepro"
        cmd = (
            f'pyinstaller --noconsole --onefile --name "{APP_NAME}" '
            f'--icon "{ICO_PATH.as_posix()}" '
            f'--manifest "build/app.manifest" '
            f'--add-data "{ASSETS.as_posix()}{os.pathsep}assets" '
            f'-m ebookforgepro.cli'
        )
        (BUILD / "build_windows.cmd").write_text(cmd, encoding="utf-8")
        (BUILD / "version.txt").write_text(APP_VERSION, encoding="utf-8")
        messagebox.showinfo("Success", "Windows build helper files written to 'build' directory.")

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
        self.image_generator = ImageGenerator()
        self.generated_cover_image = None
        self.cover_photo_image = None
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
            "Metadata": ttk.Frame(nb), "Compose": ttk.Frame(nb), "Cover Creator": ttk.Frame(nb),
            "Music": ttk.Frame(nb), "Export": ttk.Frame(nb), "Upload": ttk.Frame(nb),
            "APIs": ttk.Frame(nb), "Windows Build": ttk.Frame(nb), "Diagnostics": ttk.Frame(nb),
        }
        for name, frame in tabs.items():
            nb.add(frame, text=name)

        self._build_metadata_tab(tabs["Metadata"])
        self._build_compose_tab(tabs["Compose"])
        self._build_cover_tab(tabs["Cover Creator"])
        self._build_music_tab(tabs["Music"])
        self._build_export_tab(tabs["Export"])
        self._build_upload_tab(tabs["Upload"])
        self._build_api_tab(tabs["APIs"])
        self._build_build_tab(tabs["Windows Build"])
        self._build_diagnostics_tab(tabs["Diagnostics"])

    def _build_metadata_tab(self, tab):
        # ... (Full implementation from previous steps)
        pass

    def _build_compose_tab(self, tab):
        # ... (Full implementation from previous steps)
        pass

    def _build_cover_tab(self, tab):
        # ... (Full implementation from previous steps)
        pass

    def _build_music_tab(self, tab):
        # ... (Full implementation from previous steps)
        pass

    def _build_export_tab(self, tab):
        # ... (Full implementation from previous steps)
        pass

    def _build_upload_tab(self, tab):
        # ... (Full implementation from previous steps)
        pass

    def _build_api_tab(self, tab):
        # ... (Full implementation from previous steps)
        pass

    def _build_build_tab(self, tab):
        # ... (Full implementation from previous steps)
        pass

    def _build_diagnostics_tab(self, tab):
        self.diag_txt = tk.Text(tab, wrap="word")
        self.diag_txt.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log("Application started.")

    def log(self, msg: str):
        self.diag_txt.configure(state="normal")
        self.diag_txt.insert("end", f"{datetime.datetime.now().strftime('%H:%M:%S')} - {msg}\n")
        self.diag_txt.see("end")
        self.diag_txt.configure(state="disabled")

    def gen_draft(self):
        # ... (Full implementation from previous steps)
        pass

    def do_autonomous_generation(self):
        # ... (Full implementation from previous steps)
        pass

    def do_music_generation(self):
        # ... (Full implementation from previous steps)
        pass

    def do_image_generation(self):
        # ... (Full implementation from previous steps)
        pass

    def do_save_cover(self):
        # ... (Full implementation from previous steps)
        pass

    def save_api(self):
        # ... (Full implementation from previous steps)
        pass

    def _browse_gguf(self):
        # ... (Full implementation from previous steps)
        pass

    def self_check(self):
        # ... (Full implementation from previous steps)
        pass

    def open_project(self):
        # ... (Full implementation from previous steps)
        pass

    def load_first(self):
        # ... (Full implementation from previous steps)
        pass

    def do_clean(self):
        # ... (Full implementation from previous steps)
        pass

    def do_merge_first(self):
        # ... (Full implementation from previous steps)
        pass

    def do_ai_expand(self):
        # ... (Full implementation from previous steps)
        pass

    def refresh_preview(self):
        # ... (Full implementation from previous steps)
        pass

    def export_md(self):
        # ... (Full implementation from previous steps)
        pass

    def export_docx(self):
        # ... (Full implementation from previous steps)
        pass

    def export_epub(self):
        # ... (Full implementation from previous steps)
        pass

    def export_pdf(self):
        # ... (Full implementation from previous steps)
        pass

    def do_gumroad(self):
        # ... (Full implementation from previous steps)
        pass

    def do_kofi(self):
        # ... (Full implementation from previous steps)
        pass

    def do_onix(self):
        # ... (Full implementation from previous steps)
        pass

    def do_sftp_upload(self):
        # ... (Full implementation from previous steps)
        pass
