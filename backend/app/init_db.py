from backend.app.db import engine, Base
from backend.app.models import Prompt

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
