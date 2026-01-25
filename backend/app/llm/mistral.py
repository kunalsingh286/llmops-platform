import requests
from backend.app.llm.base import BaseLLM

class MistralLLM(BaseLLM):
    def generate(self, prompt: str) -> str:
        payload = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }

        resp = requests.post("http://localhost:11434/api/generate", json=payload)
        data = resp.json()
        return data.get("response", "")
