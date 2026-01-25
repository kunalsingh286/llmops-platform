from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime
from backend.app.db import Base

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    version = Column(Integer)
    prompt_text = Column(Text)
    status = Column(String)
    traffic_weight = Column(Float, default=1.0)

    model_name = Column(String, default="llama3")  # NEW

    created_at = Column(DateTime, default=datetime.utcnow)


class InferenceLog(Base):
    __tablename__ = "inference_logs"

    id = Column(Integer, primary_key=True)
    prompt_name = Column(String)
    prompt_version = Column(Integer)
    model_name = Column(String, default="llama3")  # NEW


    latency_ms = Column(Float)
    token_count = Column(Integer)

    cost = Column(Float)  # NEW

    created_at = Column(DateTime, default=datetime.utcnow)




class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    prompt_name = Column(String)
    prompt_version = Column(Integer)

    user_input = Column(Text)
    model_output = Column(Text)

    rating = Column(Integer)  # 1 = bad, 5 = good
    comment = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)


