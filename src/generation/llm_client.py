"""LLM client for local model inference using Ollama."""

import subprocess
from typing import List


class OllamaClient:
    """Client for interacting with Ollama local LLM."""

    def __init__(self, model_name: str = "llama3"):
        """Initialize Ollama client with model name."""
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        """Call Ollama CLI and return the generated text."""
        result = subprocess.run(
            ["ollama", "run", self.model_name],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return result.stdout.decode("utf-8")

