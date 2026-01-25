from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.db import SessionLocal
from backend.app.models import Feedback

router = APIRouter()

class FeedbackRequest(BaseModel):
    prompt_name: str
    prompt_version: int
    user_input: str
    model_output: str
    rating: int
    comment: str | None = None

@router.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    db: Session = SessionLocal()

    feedback = Feedback(
        prompt_name=request.prompt_name,
        prompt_version=request.prompt_version,
        user_input=request.user_input,
        model_output=request.model_output,
        rating=request.rating,
        comment=request.comment
    )

    db.add(feedback)
    db.commit()
    db.close()

    return {"status": "feedback stored"}
