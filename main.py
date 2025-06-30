from typing import Optional, Union
from fastapi import FastAPI, Response, status
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

def find_post(id):
    for i in my_posts:
        if id == i["id"]:
            return i


@app.get("/")
def read_root():
    return {"message": "welcome to my url lol"}

# Get all posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# Create a post
@app.post("/posts")
def create_post(post:Post):
    post_dict = post.dict()
    post_dict["id"]= randrange(0,1000)
    my_posts.append(post_dict)
    return {"data":post}

# Get ID specific post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    found_post=find_post(id)
    if not found_post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message":f"Post with id: {id} not found"}
    return {"message": found_post}
