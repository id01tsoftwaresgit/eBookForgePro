import subprocess
import sys
import importlib

def ensure_pkg(import_name: str, pip_name: str):
    """
    Checks if a package is installed, and if not, installs it using pip.
    """
    try:
        return importlib.import_module(import_name)
    except ImportError:
        print(f"[deps] Installing {pip_name}…")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
            return importlib.import_module(import_name)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {pip_name}. Please install it manually.", file=sys.stderr)
            raise e
