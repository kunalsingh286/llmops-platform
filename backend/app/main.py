from fastapi import FastAPI
from backend.app.api.generate import router as generate_router
from backend.app.api.prompts import router as prompt_router


app = FastAPI(title="LLMOps Inference Service")

app.include_router(generate_router)

app.include_router(prompt_router)
