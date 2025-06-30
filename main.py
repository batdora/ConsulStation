from typing import Optional, Union
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# For optional requests, use a defaulted field; for full optional default to None
# For str valued requests, if you use int; it converts int to str automatically. Look out.

@app.get("/")
def read_root():
    return {"message": "welcome to my url lol"}

@app.get("/posts")
def get_posts():
    return {"message": "this is your post"}

@app.post("/createpost")
def create_post(new_post:Post):
    print(new_post.published)
    new_post.dict()
    return {"data":new_post}

