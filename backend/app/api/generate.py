from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.llm.ollama_llama import OllamaLlamaProvider

router = APIRouter()
llm = OllamaLlamaProvider()

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    response: str

@router.post("/generate", response_model=GenerateResponse)
def generate_text(request: GenerateRequest):
    output = llm.generate(request.prompt)
    return {"response": output}
