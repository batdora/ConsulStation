from turtle import title
from typing import Optional, Union, Any
from fastapi import FastAPI, Response, status, HTTPException, Depends, Query
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
import signal
import sys
from app.database import engine, get_db
import app.models as models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

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

"""CRUD Operations using psycopg and SQL code"""
# GET all posts
#@app.get("/posts")
#def get_posts():
    #cur.execute("""SELECT * FROM posts""")
    #posts= cur.fetchall()
    #return {"data": posts}

# CREATE a post
#@app.post("/posts", status_code=status.HTTP_201_CREATED)
#def create_post(post:Post):
    #cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    #new_post = cur.fetchone()
    #conn.commit()
    #return {"data":new_post}

# GET ID specific post
#@app.get("/posts/{id}")
#def get_post(id: int):
    #cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) # type: ignore
    #post = cur.fetchone()
    #if not post:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")
    #return {"message": post}

# DELETE Post
#@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
#def delete_post(id: int):
    #cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),)) # type: ignore
    #post = cur.fetchone()
    #conn.commit()
    #if not post:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")
    #else:
    #    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# Update with PUT
#@app.put("/posts/{id}")
#def update_post_1(id: int, post: Post):
    #cur.execute("""UPDATE posts SET title= %s, content= %s, published= %s WHERE id = %s RETURNING *""", (post.title,post.content,str(post.published),str(id)))
    #updated_post = cur.fetchone() # type: ignore
    #conn.commit()
    #if not updated_post:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")
    #return {"data":updated_post}


"""CRUD Operations using SQLAlchemy"""

# GET all posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

# GET ID specific post
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")
    return {"data": post}

# POST a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

# DELETE Post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update with PUT
@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")
    
    updated_post.update(post.model_dump(), synchronize_session=False) # type: ignore
    db.commit()
    return {"data": updated_post.first()}