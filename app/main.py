from typing import Optional, Union, Any
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
import signal
import sys

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Define SIGINT handler
def handle_interrupt(signum, frame):
    print("\n KeyboardInterrupt caught. Exiting.")
    sys.exit(0)
# Register the handler
signal.signal(signal.SIGINT, handle_interrupt)

# Fetch Password from file
with open("app/db_credentials.txt", "r") as f:
        db_password = f.read().strip()


while True:
    try:
        conn = psycopg.connect(
            host="localhost",
            dbname="fastapi",
            user="postgres",
            password=db_password,
            row_factory=dict_row  # type: ignore
        )
        cur = conn.cursor()
        print("Database Connection SUCCESSFUL")
        break
    except Exception as error:
        print("Connection to Database FAILED")
        print("Error :", error)
        time.sleep(2)


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
    cur.execute("""SELECT * FROM posts""")
    posts= cur.fetchall()
    return {"data": posts}

# CREATE a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    new_post = cur.fetchone()
    conn.commit()
    return {"data":new_post}

# GET ID specific post
@app.get("/posts/{id}")
def get_post(id: int):
    cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) # type: ignore
    post = cur.fetchone()
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