from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.db import SessionLocal
from backend.app.models import Prompt

router = APIRouter()

class CanaryRequest(BaseModel):
    name: str
    version: int
    traffic_weight: float

@router.post("/canary")
def set_canary(request: CanaryRequest):
    db: Session = SessionLocal()

    prompt = (
        db.query(Prompt)
        .filter(Prompt.name == request.name, Prompt.version == request.version)
        .first()
    )

    if not prompt:
        db.close()
        return {"error": "Prompt not found"}

    prompt.traffic_weight = request.traffic_weight
    prompt.status = "active"

    db.commit()
    db.close()

    return {"status": "canary updated"}
