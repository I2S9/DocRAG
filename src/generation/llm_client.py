"""LLM client for local model inference using Ollama."""

import subprocess
from typing import List


class OllamaClient:
    """Client for interacting with Ollama local LLM."""

    def __init__(self, model_name: str = "llama3"):
        """Initialize Ollama client with model name."""
        self.model_name = model_name

    def generate(self, prompt: str, timeout: int = 300) -> str:
        """Call Ollama CLI and return the generated text."""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                timeout=timeout,
            )
            output = result.stdout.decode("utf-8")
            if not output.strip():
                error_msg = result.stderr.decode("utf-8") if result.stderr else "No output from Ollama"
                raise RuntimeError(f"Ollama returned empty output. Error: {error_msg}")
            return output
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Ollama generation timed out after {timeout} seconds")
        except FileNotFoundError:
            raise FileNotFoundError(
                "Ollama not found. Please install Ollama from https://ollama.ai/ and ensure it's in your PATH."
            )
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode("utf-8") if e.stderr else str(e)
            raise RuntimeError(f"Ollama error: {error_msg}")

