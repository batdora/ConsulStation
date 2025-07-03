from fastapi import FastAPI, Response, status, HTTPException, Depends, Query
from app.database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, utils
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

# Define a root endpoint
@app.get("/")
def read_root():
    return {"message": "welcome to my url lol"}
