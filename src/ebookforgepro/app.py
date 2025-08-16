import os
import sys
import json
import subprocess
import threading
import traceback
import datetime
from pathlib import Path

# GUI Toolkit
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as tb

# Local application imports
from .core import (
    APP_NAME, APP_VERSION, APP_ID, PROJECT_DIR, ASSETS, BUILD, ICO_PATH, TRAINING_DATA,
    scaffold_from_meta, autonomous_generation, clean_text
)
from .ai import Expander
from .exporters import Exporter
from .uploaders import Uploader

class WinHelpers:
    @staticmethod
    def write_all():
        BUILD.mkdir(parents=True, exist_ok=True)
        ASSETS.mkdir(parents=True, exist_ok=True)
        if not ICO_PATH.exists():
            try:
                from .core import EMBED_ICO
                ICO_PATH.write_bytes(base64.b64decode(EMBED_ICO))
            except Exception: pass
        # ... (rest of the build helper logic) ...

class App(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry("1240x840")
        self.minsize(1080, 720)
        try:
            if ICO_PATH.exists(): self.iconbitmap(ICO_PATH)
        except Exception: pass

        self.api_cfg = self._load_api_settings()
        self.first_text = ""
        self._build_ui()

    def _load_api_settings(self):
        # ... (same as before, but with llama_cpp_model_path) ...
        defaults = {
            "mode": "offline", "openai_api_key": "", "openai_model": "gpt-4o-mini",
            "openai_base": "https://api.openai.com/v1", "gemini_api_key": "", "gemini_model": "gemini-1.5-flash",
            "local_base": "http://127.0.0.1:11434", "local_model": "llama3", "llama_cpp_model_path": ""
        }
        settings_file = PROJECT_DIR / "api_settings.json"
        if settings_file.exists():
            try:
                with open(settings_file, "r") as f:
                    loaded_settings = json.load(f)
                    return {**defaults, **loaded_settings}
            except Exception: pass
        return defaults

    def _build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True)
        # ... (code to create all the tabs) ...
        self._build_api_tab(ttk.Frame(nb)) # Simplified for brevity
        # ...

    def _build_api_tab(self, tab):
        # ... (Full API tab buildout as in my previous attempt) ...
        self.mode_var = tk.StringVar(value=self.api_cfg.get("mode"))
        # ... Radiobuttons ...
        self.oai_key = tk.StringVar(value=self.api_cfg.get("openai_api_key"))
        # ... other StringVars ...
        self.lcpp_path = tk.StringVar(value=self.api_cfg.get("llama_cpp_model_path", ""))
        # ... Full grid layout ...
        ttk.Button(tab, text="Save API settings", command=self.save_api).pack(anchor="e")

    def save_api(self):
        self.api_cfg.update({
            "mode": self.mode_var.get(),
            "openai_api_key": self.oai_key.get().strip(),
            "openai_model": self.oai_model.get().strip(),
            "openai_base": self.oai_base.get().strip(),
            "gemini_api_key": self.gm_key.get().strip(),
            "gemini_model": self.gm_model.get().strip(),
            "local_base": self.loc_base.get().strip(),
            "local_model": self.loc_model.get().strip(),
            "llama_cpp_model_path": self.lcpp_path.get().strip(),
        })
        settings_file = PROJECT_DIR / "api_settings.json"
        settings_file.parent.mkdir(parents=True, exist_ok=True)
        with open(settings_file, "w") as f:
            json.dump(self.api_cfg, f, indent=2)
        messagebox.showinfo(APP_NAME, "API settings saved")

    def _browse_gguf(self):
        path = filedialog.askopenfilename(filetypes=[("GGUF Model Files", "*.gguf")])
        if path:
            self.lcpp_path.set(path)

    # ... (All other methods like gen_draft, do_autonomous_generation, etc.) ...
    def gen_draft(self):
        pass # Placeholder for brevity
    def do_autonomous_generation(self):
        pass # Placeholder for brevity
