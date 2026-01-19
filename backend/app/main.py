from fastapi import FastAPI
from backend.app.api.generate import router as generate_router

app = FastAPI(title="LLMOps Inference Service")

app.include_router(generate_router)
