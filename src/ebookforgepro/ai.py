import os
import sys
import json
import requests
import importlib

from .core import clean_text

class Expander:
    def __init__(self, cfg: dict):
        self.cfg = cfg

    def expand(self, manuscript: str) -> str:
        mode = self.cfg.get("mode", "offline")
        try:
            if mode == "offline":
                # In autonomous mode, "offline" isn't useful, return a placeholder.
                if "You are an expert author" in manuscript:
                    return "## Chapter Content\n\nOffline mode cannot generate new content. Please select an AI provider in the APIs tab."
                return manuscript
            if mode == "openai":
                return self._openai_like(manuscript)
            if mode == "gemini":
                return self._gemini(manuscript)
            if mode == "local":
                return self._ollama(manuscript)
            if mode == "llama.cpp":
                return self._llama_cpp(manuscript)
        except Exception as e:
            print(f"[expander] error, fallback to offline: {e}")
        return manuscript

    def _openai_like(self, manuscript: str) -> str:
        key = self.cfg.get("openai_api_key")
        base = self.cfg.get("openai_base", "https://api.openai.com/v1")
        model = self.cfg.get("openai_model", "gpt-4o-mini")
        if not key and "127.0.0.1" not in base: # Allow keyless for local servers
            return manuscript

        url = f"{base}/chat/completions"
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

        # The 'manuscript' is now the detailed prompt from the generation functions
        payload = {"model": model, "messages": [{"role": "user", "content": manuscript}], "temperature": 0.4}

        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=240)
        r.raise_for_status()
        out = r.json().get("choices", [{}])[0].get("message", {}).get("content", manuscript)
        return clean_text(out)

    def _gemini(self, manuscript: str) -> str:
        key = self.cfg.get("gemini_api_key")
        model = self.cfg.get("gemini_model", "gemini-1.5-flash")
        if not key:
            return manuscript

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        payload = {"contents": [{"parts": [{"text": manuscript}]}]}
        r = requests.post(url, json=payload, timeout=240)
        r.raise_for_status()
        data = r.json()
        try:
            return clean_text(data["candidates"][0]["content"]["parts"][0]["text"])
        except Exception:
            return manuscript

    def _ollama(self, manuscript: str) -> str:
        base = self.cfg.get("local_base", "http://127.0.0.1:11434")
        model = self.cfg.get("local_model", "llama3")
        url = f"{base}/api/generate"
        # The 'manuscript' is the prompt
        payload = {"model": model, "prompt": manuscript, "stream": False}
        r = requests.post(url, json=payload, timeout=300)
        r.raise_for_status()
        return clean_text(r.json().get("response", manuscript))

    def _llama_cpp(self, manuscript: str) -> str:
        model_path = self.cfg.get("llama_cpp_model_path")
        if not model_path or not os.path.exists(model_path):
            return "Error: Llama.cpp model path not found or not specified. Please configure it in the APIs tab."

        try:
            llama_cpp = ensure_pkg("llama_cpp", "llama-cpp-python")
        except Exception as e:
            return f"Error: Failed to install or import llama-cpp-python. Please install it with 'pip install ebookforgepro[local_llm]'. Details: {e}"

        llm = llama_cpp.Llama(model_path=model_path, n_ctx=4096, verbose=False)

        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": "You are an expert author."},
                {"role": "user", "content": manuscript}
            ],
            temperature=0.5,
        )

        return clean_text(response['choices'][0]['message']['content'])
