from backend.app.llm.llama import LlamaLLM
from backend.app.llm.mistral import MistralLLM

def get_llm(model_name: str):
    if model_name == "llama3":
        return LlamaLLM()
    elif model_name == "mistral":
        return MistralLLM()
    else:
        raise ValueError(f"Unknown model: {model_name}")

