"""Ollama implementation of the LLM provider interface."""

import requests
from ollama import Client


class OllamaProvider:
    def __init__(self, model: str, base_url: str, timeout: int = 60):
        self.model = model
        self.client = Client(host=base_url, timeout=timeout)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.message.content or ""

    def model_exist(self, url: str) -> bool:
        try:
            response = requests.get(f"{url.rstrip('/')}/api/tags", timeout=5)
            response.raise_for_status()
            models = response.json().get("models", [])
            return any(model.get("name") == self.model for model in models)
        except (requests.RequestException, ValueError, TypeError):
            return False

    def check_ollama_running(self, url: str) -> bool:
        try:
            response = requests.get(f"{url.rstrip('/')}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
