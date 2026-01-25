import time
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.llm.ollama_llama import OllamaLlamaProvider
from backend.app.db import SessionLocal
from backend.app.models import Prompt, InferenceLog
from backend.app.utils import estimate_tokens

router = APIRouter()
llm = OllamaLlamaProvider()

class GenerateRequest(BaseModel):
    prompt_name: str
    user_input: str

@router.post("/generate")
def generate_text(request: GenerateRequest):
    db: Session = SessionLocal()

    prompt = (
        db.query(Prompt)
        .filter(Prompt.name == request.prompt_name, Prompt.status == "active")
        .first()
    )

    if not prompt:
        db.close()
        return {"error": "No active prompt found"}

    # 🔒 Extract values BEFORE session closes
    prompt_name = prompt.name
    prompt_version = prompt.version
    prompt_text = prompt.prompt_text

    full_prompt = f"{prompt_text}\nUser: {request.user_input}"

    start_time = time.time()
    response = llm.generate(full_prompt)
    latency_ms = (time.time() - start_time) * 1000

    token_count = estimate_tokens(full_prompt + response)

    log = InferenceLog(
        prompt_name=prompt_name,
        prompt_version=prompt_version,
        model_name="llama3",
        latency_ms=latency_ms,
        token_count=token_count
    )

    db.add(log)
    db.commit()
    db.close()

    return {
        "prompt_version": prompt_version,
        "latency_ms": latency_ms,
        "tokens": token_count,
        "response": response
    }
