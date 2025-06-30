from typing import Optional, Union, Any
from fastapi import FastAPI, Response, status, HTTPException
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

# GET all posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# CREATE a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    post_dict = post.dict()
    post_dict["id"]= randrange(0,1000)
    my_posts.append(post_dict)
    return {"data":post}

# GET ID specific post
@app.get("/posts/{id}")
def get_post(id: int):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")
    return {"message": post}

# DELETE Post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")
    else:
        my_posts.remove(post)
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
# Update with PUT
@app.put("/posts/{id}")
def update_post_1(id: int, updated_post: Post):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")
    updated_post_dict= updated_post.dict()
    updated_post_dict["id"] = id
    index = my_posts.index(post)
    my_posts[index] = updated_post_dict
    return {"data":updated_post_dict}

# Update with PATCH
@app.patch("/posts/{id}")
def update_post_2(id: int, updated_part: dict):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")
    
    for key, value in updated_part.items():
        if key in post:
            post[key] = value

    return {"data":post}