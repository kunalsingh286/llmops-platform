from fastapi import FastAPI
from backend.app.api.generate import router as generate_router
from backend.app.api.prompts import router as prompt_router
from backend.app.api.feedback import router as feedback_router


app = FastAPI(title="LLMOps Inference Service")

app.include_router(generate_router)

app.include_router(prompt_router)

app.include_router(feedback_router)

