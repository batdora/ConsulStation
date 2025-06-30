from typing import Optional, Union
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts=[{"title":"title1", "content":"content 1", "id": 1},{"title":"title 2", "content":"content 2", "id": 2} ]

@app.get("/")
def read_root():
    return {"message": "welcome to my url lol"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_post(post:Post):
    post_dict = post.dict()
    post_dict["id"]= randrange(0,1000)
    my_posts.append(post_dict)
    return {"data":post}

