import datetime
from .core import EXPORTS, slugify
from .dependencies import ensure_pkg

class MusicGenerator:
    """
    Handles the generation of music from text prompts using Hugging Face Transformers.
    """
    def __init__(self):
        self.model = None
        self.processor = None
        self.device = None

    def _load_model(self):
        """Loads the MusicGen model and processor on demand."""
        if self.model is not None and self.processor is not None:
            return

        print("[MusicGen] Loading model... This may take a while and consume significant memory.")

        # Ensure dependencies are available
        torch = ensure_pkg("torch", "torch")
        transformers = ensure_pkg("transformers", "transformers")

        # Set device
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        print(f"[MusicGen] Using device: {self.device}")

        # Load model and processor
        try:
            self.processor = transformers.AutoProcessor.from_pretrained("facebook/musicgen-small")
            self.model = transformers.MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(self.device)
            print("[MusicGen] Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load MusicGen model: {e}")
            self.model = None
            self.processor = None
            raise  # Re-raise the exception to be caught by the caller

    def generate(self, prompt: str, duration: int = 10):
        """
        Generates a music tensor from a prompt.
        Returns the raw audio tensor.
        """
        self._load_model()
        if not self.model or not self.processor:
            raise RuntimeError("MusicGen model is not loaded.")

        print(f"[MusicGen] Generating music for prompt: '{prompt}' ({duration}s)")

        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        ).to(self.device)

        sampling_rate = self.model.config.audio_encoder.sampling_rate
        max_new_tokens = int(duration * sampling_rate / 256)

        audio_values = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
        return audio_values, sampling_rate

    def save_wav(self, audio_values, sampling_rate: int, prompt: str) -> str:
        """Saves the generated audio data to a WAV file."""
        print("[MusicGen] Processing and saving audio...")
        # Process the tensor here
        processed_audio = audio_values[0, 0].cpu().numpy()
        return self._save_wav(processed_audio, sampling_rate, prompt)

    def _save_wav(self, audio_data, sampling_rate: int, prompt: str) -> str:
        """Saves the generated audio data to a WAV file."""
        scipy_wavfile = ensure_pkg("scipy.io.wavfile", "scipy")

        EXPORTS.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"music_{slugify(prompt)[:50]}_{timestamp}.wav"
        filepath = EXPORTS / filename

        # Normalize and convert to 16-bit PCM
        audio_data_int16 = (audio_data * 32767).astype("int16")

        scipy_wavfile.write(filepath, rate=sampling_rate, data=audio_data_int16)
        print(f"[MusicGen] Saved music to {filepath}")
        return str(filepath)
