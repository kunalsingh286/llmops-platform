import requests
from backend.app.llm.base import BaseLLM

class LlamaLLM(BaseLLM):
    def generate(self, prompt: str) -> str:
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }

        resp = requests.post("http://localhost:11434/api/generate", json=payload)
        data = resp.json()
        return data.get("response", "")
