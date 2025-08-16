import datetime
from .core import EXPORTS, slugify
from .dependencies import ensure_pkg

class ImageGenerator:
    """
    Handles the generation of images from text prompts using Hugging Face Diffusers.
    """
    def __init__(self):
        self.pipeline = None
        self.device = None

    def _load_model(self):
        """Loads the Stable Diffusion model pipeline on demand."""
        if self.pipeline is not None:
            return

        print("[ImageGen] Loading model... This may take a while and require a large download.")

        # Ensure dependencies are available
        torch = ensure_pkg("torch", "torch")
        ensure_pkg("accelerate", "accelerate")
        diffusers = ensure_pkg("diffusers", "diffusers")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[ImageGen] Using device: {self.device}")

        # Load model pipeline
        try:
            self.pipeline = diffusers.DiffusionPipeline.from_pretrained(
                "stabilityai/stable-diffusion-2-1-base",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            )
            self.pipeline.to(self.device)
            print("[ImageGen] Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load Stable Diffusion model: {e}")
            self.pipeline = None
            raise

    def generate(self, prompt: str):
        """
        Generates an image from a prompt.
        Returns a PIL Image object.
        """
        self._load_model()
        if not self.pipeline:
            raise RuntimeError("Stable Diffusion pipeline is not loaded.")

        print(f"[ImageGen] Generating image for prompt: '{prompt}'")

        # The pipeline returns an object with an `images` attribute, which is a list of PIL images.
        result = self.pipeline(prompt=prompt)
        image = result.images[0]

        print("[ImageGen] Image generation complete.")
        return image

    def save_image(self, image, prompt: str) -> str:
        """Saves the generated PIL Image to a PNG file."""
        EXPORTS.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cover_{slugify(prompt)[:50]}_{timestamp}.png"
        filepath = EXPORTS / filename

        image.save(filepath, "PNG")
        print(f"[ImageGen] Saved image to {filepath}")
        return str(filepath)
