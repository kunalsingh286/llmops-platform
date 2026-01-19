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

class InferenceLog(Base):
    __tablename__ = "inference_logs"

    id = Column(Integer, primary_key=True)
    prompt_name = Column(String)
    prompt_version = Column(Integer)

    model_name = Column(String)
    latency_ms = Column(Float)
    token_count = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

