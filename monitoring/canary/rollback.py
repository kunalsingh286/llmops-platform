from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np

from backend.app.models import Prompt, Feedback

DATABASE_URL = "postgresql://llmops:llmops@localhost:5432/llmops"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()

# Compare feedback scores
prompts = db.query(Prompt).filter(Prompt.status == "active").all()

for p in prompts:
    scores = (
        db.query(Feedback.rating)
        .filter(Feedback.prompt_name == p.name, Feedback.prompt_version == p.version)
        .all()
    )

    if not scores:
        continue

    avg_score = np.mean([s[0] for s in scores])

    if avg_score < 3:
        print(f"Rolling back prompt {p.name} v{p.version}")
        p.status = "inactive"
        p.traffic_weight = 0.0

db.commit()
db.close()

print("Canary rollback check complete.")
