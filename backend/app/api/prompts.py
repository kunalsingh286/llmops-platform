from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.db import SessionLocal
from backend.app.models import Prompt

router = APIRouter(prefix="/prompts")

class PromptCreate(BaseModel):
    name: str
    prompt_text: str

@router.post("/")
def create_prompt(data: PromptCreate):
    db: Session = SessionLocal()

    latest = (
        db.query(Prompt)
        .filter(Prompt.name == data.name)
        .order_by(Prompt.version.desc())
        .first()
    )

    version = 1 if not latest else latest.version + 1

    prompt = Prompt(
        name=data.name,
        version=version,
        prompt_text=data.prompt_text,
        status="inactive"
    )

    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    db.close()

    return {"id": prompt.id, "version": version}


@router.post("/{prompt_id}/activate")
def activate_prompt(prompt_id: int):
    db: Session = SessionLocal()

    prompt = db.query(Prompt).get(prompt_id)
    if not prompt:
        return {"error": "Prompt not found"}

    # deactivate all other versions of the same prompt
    db.query(Prompt).filter(
        Prompt.name == prompt.name
    ).update({"status": "inactive", "traffic_percentage": 0.0})

    prompt.status = "active"
    prompt.traffic_percentage = 100.0

    db.commit()
    db.close()

    return {"message": "Prompt activated successfully"}
