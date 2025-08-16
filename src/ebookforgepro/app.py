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

class App(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry("1240x840")
        # ... (other init code) ...
        self.image_generator = ImageGenerator()
        self.generated_cover_image = None # To hold PIL.Image object
        self.cover_photo_image = None # To hold PhotoImage object
        self._build_ui()

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
        # ... (call other build methods) ...

    def _build_cover_tab(self, tab):
        container = ttk.Frame(tab, padding=15)
        container.pack(fill=tk.BOTH, expand=True)

        # Top frame for prompt and button
        top_frame = ttk.Frame(container)
        top_frame.pack(fill=tk.X, pady=5)

        self.cover_prompt_var = tk.StringVar(value="A majestic lion on a cosmic background, digital art")
        ttk.Label(top_frame, text="Prompt:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(top_frame, textvariable=self.cover_prompt_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(top_frame, text="Generate Image", command=self.do_image_generation, bootstyle="success").pack(side=tk.LEFT, padx=5)

        # Bottom frame for image display and save button
        bottom_frame = ttk.Frame(container)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.cover_canvas = ttk.Label(bottom_frame, text="Your generated cover will appear here.", anchor="center")
        self.cover_canvas.pack(fill=tk.BOTH, expand=True, pady=5)

        self.save_cover_button = ttk.Button(bottom_frame, text="Save Cover", command=self.do_save_cover, state="disabled")
        self.save_cover_button.pack()

    def do_image_generation(self):
        prompt = self.cover_prompt_var.get()
        if not prompt:
            messagebox.showwarning("Input Required", "Please enter an image prompt.")
            return

        self.config(cursor="wait")
        self.cover_canvas.config(text="Generating... This may take a few minutes.")
        self.update_idletasks()

        def task():
            try:
                self.log(f"Starting image generation for prompt: {prompt}")
                image = self.image_generator.generate(prompt)
                self.generated_cover_image = image # Store the PIL image

                # Resize for display if it's too large
                w, h = image.size
                max_size = 512
                if w > max_size or h > max_size:
                    ratio = min(max_size/w, max_size/h)
                    image = image.resize((int(w*ratio), int(h*ratio)), Image.Resampling.LANCZOS)

                # Convert to PhotoImage for tkinter
                self.cover_photo_image = ImageTk.PhotoImage(image)
                self.cover_canvas.config(image=self.cover_photo_image, text="")
                self.save_cover_button.config(state="normal")
                self.log("Image generation complete.")
            except Exception as e:
                self.log(f"Image generation failed: {e}")
                self.cover_canvas.config(text=f"Error: {e}")
            finally:
                self.config(cursor="")

        threading.Thread(target=task, daemon=True).start()

    def do_save_cover(self):
        if not self.generated_cover_image:
            messagebox.showwarning("No Image", "No image has been generated yet.")
            return

        try:
            prompt = self.cover_prompt_var.get()
            filepath = self.image_generator.save_image(self.generated_cover_image, prompt)
            messagebox.showinfo("Success", f"Cover image saved to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Save Failed", f"Could not save the image: {e}")

    # ... (rest of the App class methods) ...
    def log(self, msg):
        print(msg) # Simplified for this context
