from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.llm.ollama_llama import OllamaLlamaProvider
from backend.app.db import SessionLocal
from backend.app.models import Prompt

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
        return {"error": "No active prompt found"}

    full_prompt = f"{prompt.prompt_text}\nUser: {request.user_input}"

    response = llm.generate(full_prompt)

    db.close()

    return {
        "prompt_version": prompt.version,
        "response": response
    }
