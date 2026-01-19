from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime
from backend.app.db import Base

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    version = Column(Integer)
    prompt_text = Column(Text)

    status = Column(String, default="inactive")  
    traffic_percentage = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)
