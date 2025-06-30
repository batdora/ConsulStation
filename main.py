# source venvFastAPI/bin/activate
from typing import Union
from typing import Any
from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "welcome to my url lol"}

@app.get("/posts")
def get_posts():
    return {"data": "this is your post"}

@app.post("/createpost")
def create_post(payLoad:dict = Body(...)):
    print(payLoad)
    return {"new_post": f"successfully created post with title: {payLoad['title']} & content: {payLoad['content']}"}

