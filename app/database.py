from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Fetch Password from file
with open("app/db_credentials.txt", "r") as f:
        db_password = f.read().strip()

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://postgres:{db_password}@localhost:5432/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()