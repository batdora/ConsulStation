# source venvFastAPI/bin/activate
from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message":"welcome to my url lol"}

@app.get("/posts")
def get_posts():
    return {"data":"this is your post"}