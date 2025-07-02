from sqlmodel import create_engine, Session
from fastapi import Depends
from typing import Annotated

# Fetch Password from file
with open("app/db_credentials.txt", "r") as f:
        db_password = f.read().strip()

database_url = f"postgresql+psycopg://postgres:{db_password}@localhost:5432/fastapi"

engine = create_engine(database_url)

# Create what talks to the DB
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]